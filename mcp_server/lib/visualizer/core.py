"""
Visualizer Engine - Core Orchestrator
Auto-generates visual diagrams for project onboarding

OPTIMIZATIONS:
- Extracted prompts for easier maintenance
- Ready for modular refactoring (dependency_analyzer, feature_mapper, etc.)
"""

import ast
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict

# Preserving your framework utility imports
from lib.utils import detect_language, read_file_safe, get_timestamp
from lib.visualizer.prompts import build_feature_flow_prompt, build_project_concept_prompt



class VisualizerEngine:
    """Production-grade visualization generator for project onboarding"""

    def __init__(self, watsonx_client):
        self.watsonx = watsonx_client

    def _get_file_content(self, filepath: str) -> str:
        """Safely extracts text content, handling if read_file_safe returns a Tuple"""
        result = read_file_safe(filepath)
        # If your util returns (content, error_msg), grab just the content
        if isinstance(result, tuple):
            return result[0] if result[0] else ""
        return result if result else ""

    # ------------------------------------------------------------------ #
    #                     DEPENDENCY CHAIN ANALYZER                      #
    # ------------------------------------------------------------------ #

    async def generate_dependency_chain(
        self,
        project_path: str,
        output_path: Optional[str] = None,
        max_depth: int = 3,
        include_external: bool = False
    ) -> Dict[str, Any]:
        """Generate a dependency chain diagram showing grouped module relationships."""
        try:
            target_path = Path(project_path).resolve()
            if not target_path.exists():
                return {"success": False, "error": f"Project path does not exist: {target_path}"}

            local_roots = {p.name for p in target_path.iterdir() if p.is_dir() and not p.name.startswith(('.', '__'))}
            local_roots.add(target_path.name)

            dependencies = self._analyze_dependencies(target_path, max_depth, include_external, local_roots)
            mermaid_diagram = self._create_dependency_mermaid(dependencies)
            markdown = self._format_dependency_output(mermaid_diagram, dependencies, target_path)

            save_path = self._save_visualization(markdown, output_path, "dependency-chain") if output_path else None

            return {
                "success": True,
                "diagram_type": "dependency_chain",
                "markdown": markdown,
                "mermaid": mermaid_diagram,
                "saved_to": save_path,
                "stats": {
                    "total_modules": len(dependencies["modules"]),
                    "total_dependencies": len(dependencies["edges"]),
                    "external_deps": len(dependencies["external"])
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to generate dependency chain: {str(e)}"}

    def _analyze_dependencies(self, target_path: Path, max_depth: int, include_external: bool, local_roots: Set[str]) -> Dict[str, Any]:
        modules = {}
        edges = []
        external = set()
        
        python_files = [f for f in target_path.rglob("*.py") if not any(k in f.parts for k in ("__pycache__", "venv", ".venv", "env"))]
        
        for file_path in python_files:
            module_name = self._get_module_name(file_path, target_path)
            if len(module_name.split('.')) > max_depth:
                continue
                
            modules[module_name] = str(file_path.relative_to(target_path))
            imports = self._parse_imports(file_path, local_roots)
            
            for imp in imports:
                if imp["is_external"]:
                    if include_external:
                        external.add(imp["module"])
                        edges.append((module_name, imp["module"], imp["type"]))
                else:
                    edges.append((module_name, imp["module"], imp["type"]))
        
        return {"modules": modules, "edges": edges, "external": list(external)}

    def _parse_imports(self, file_path: Path, local_roots: Set[str]) -> List[Dict[str, Any]]:
        imports = []
        content = self._get_file_content(str(file_path))
        if not content:
            return imports

        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base_mod = alias.name.split('.')[0]
                        imports.append({"module": base_mod, "full_name": alias.name, "type": "import", "is_external": base_mod not in local_roots})
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        base_mod = node.module.split('.')[0]
                        imports.append({"module": base_mod, "full_name": node.module, "type": "from", "is_external": base_mod not in local_roots and not node.level > 0})
        except Exception:
            imports = self._parse_imports_regex(content, local_roots)
        return imports

    def _parse_imports_regex(self, content: str, local_roots: Set[str]) -> List[Dict[str, Any]]:
        imports = []
        pattern = r'^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))'
        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                module = match.group(1) or match.group(2)
                base_mod = module.split('.')[0]
                imports.append({"module": base_mod, "full_name": module, "type": "from" if match.group(1) else "import", "is_external": base_mod not in local_roots})
        return imports

    def _get_module_name(self, file_path: Path, project_root: Path) -> str:
        rel_path = file_path.relative_to(project_root)
        module_parts = list(rel_path.parts[:-1]) + [rel_path.stem]
        if module_parts and module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]
        return ".".join(module_parts) if module_parts else "root"

    # Maximum nodes before auto-chunking kicks in
    MAX_DIAGRAM_NODES = 15

    # Cluster color palette for overview and detail diagrams
    CLUSTER_COLORS = [
        {"fill": "#3b82f6", "stroke": "#2563eb", "label": "Blue"},
        {"fill": "#8b5cf6", "stroke": "#7c3aed", "label": "Purple"},
        {"fill": "#f97316", "stroke": "#ea580c", "label": "Orange"},
        {"fill": "#10b981", "stroke": "#059669", "label": "Green"},
        {"fill": "#f43f5e", "stroke": "#e11d48", "label": "Rose"},
        {"fill": "#06b6d4", "stroke": "#0891b2", "label": "Cyan"},
        {"fill": "#eab308", "stroke": "#ca8a04", "label": "Amber"},
        {"fill": "#64748b", "stroke": "#475569", "label": "Slate"},
    ]

    THEME_CONFIG = (
        "%%{init: {'theme': 'base', 'themeVariables': {"
        " 'fontFamily': 'Inter, Segoe UI, sans-serif'"
        "}}}%%"
    )

    def _create_dependency_mermaid(self, dependencies: Dict[str, Any]) -> str:
        """Route to single or chunked diagram based on module count."""
        total_nodes = len(dependencies["modules"])
        if total_nodes > self.MAX_DIAGRAM_NODES:
            return self._create_chunked_dependency_diagrams(dependencies)
        return self._create_single_dependency_mermaid(dependencies)

    # ------------------------------------------------------------------ #
    #                  SINGLE DIAGRAM (small projects)                    #
    # ------------------------------------------------------------------ #

    def _create_single_dependency_mermaid(self, dependencies: Dict[str, Any]) -> str:
        """Generate a single dependency diagram for small projects."""

        layer_styles = {
            "Root":        {"fill": "#1e293b", "stroke": "#3b82f6", "text": "#e2e8f0"},
            "lib":         {"fill": "#1a1a2e", "stroke": "#a78bfa", "text": "#e2e8f0"},
            "tests":       {"fill": "#1c1917", "stroke": "#fb923c", "text": "#e2e8f0"},
            "dataset_bob": {"fill": "#0f172a", "stroke": "#34d399", "text": "#e2e8f0"},
        }
        default_style = {"fill": "#1e1e2e", "stroke": "#64748b", "text": "#e2e8f0"}

        lines = ["```mermaid", self.THEME_CONFIG, "graph TD"]

        # Group modules into layer subgraphs
        subgraphs = defaultdict(list)
        for module_name in dependencies["modules"].keys():
            root_part = module_name.split('.')[0] if '.' in module_name else "Root"
            subgraphs[root_part].append(module_name)

        for group, elements in subgraphs.items():
            label = group.upper().replace("_", " ")
            lines.append(f"    subgraph {group} [{label}]")
            lines.append(f"    direction TB")
            for mod in elements:
                safe_id = mod.replace(".", "_")
                display_name = mod.split(".")[-1]
                lines.append(f"        {safe_id}([{display_name}])")
            lines.append("    end")

        # External packages — collapsed single node
        ext_list = dependencies.get("external", [])
        if ext_list:
            ext_label = " | ".join(sorted(ext_list))
            lines.append(f'    ext_deps[/"{ext_label}"\\]')

        # Internal edges
        added_edges = set()
        ext_sources = set()
        for from_mod, to_mod, imp_type in dependencies["edges"]:
            from_id = from_mod.replace(".", "_")
            if to_mod in ext_list:
                ext_sources.add(from_id)
            else:
                to_id = to_mod.replace(".", "_")
                edge_key = (from_id, to_id)
                if edge_key not in added_edges and from_id != to_id:
                    lines.append(f"    {from_id} --> {to_id}")
                    added_edges.add(edge_key)

        # External edges
        if ext_list:
            for src_id in sorted(ext_sources):
                lines.append(f"    {src_id} -.-> ext_deps")

        # Class definitions
        lines.append("")
        lines.append("    classDef coreNode fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef libNode fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef testNode fill:#f97316,stroke:#ea580c,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef extNode fill:#0d9488,stroke:#0f766e,stroke-width:2px,color:#fff,rx:6")

        for group, elements in subgraphs.items():
            cls = "coreNode" if group == "Root" else "testNode" if group == "tests" else "libNode"
            for mod in elements:
                safe_id = mod.replace(".", "_")
                lines.append(f"    class {safe_id} {cls}")

        if ext_list:
            lines.append("    class ext_deps extNode")

        # Subgraph styling
        lines.append("")
        for group in subgraphs.keys():
            s = layer_styles.get(group, default_style)
            lines.append(f"    style {group} fill:{s['fill']},stroke:{s['stroke']},stroke-width:2px,color:{s['text']},rx:12")

        # Link styles
        internal_count = len(added_edges)
        ext_edge_count = len(ext_sources)
        if internal_count > 0:
            internal_indices = ",".join(str(i) for i in range(internal_count))
            lines.append(f"    linkStyle {internal_indices} stroke:#60a5fa,stroke-width:2px")
        if ext_edge_count > 0:
            ext_indices = ",".join(str(i) for i in range(internal_count, internal_count + ext_edge_count))
            lines.append(f"    linkStyle {ext_indices} stroke:#2dd4bf,stroke-width:1.5px,stroke-dasharray:5")

        lines.append("```")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #               CHUNKED DIAGRAMS (large projects)                     #
    # ------------------------------------------------------------------ #

    def _get_cluster_key(self, mod_name: str) -> str:
        """Map a module name to its cluster key (2nd-level grouping)."""
        parts = mod_name.split('.')
        if len(parts) >= 3:
            return '.'.join(parts[:2])   # lib.qa_sentry.core -> lib.qa_sentry
        elif len(parts) == 2:
            return parts[0]              # lib.formatters -> lib
        return "root"                    # server -> root

    def _cluster_modules(self, modules: Dict[str, Any]) -> Dict[str, list]:
        """Group modules into logical clusters by second-level package."""
        clusters = defaultdict(list)
        for mod_name in modules.keys():
            clusters[self._get_cluster_key(mod_name)].append(mod_name)
        return dict(clusters)

    def _cluster_display_name(self, cluster_name: str) -> str:
        """Convert a cluster key to a human-readable title."""
        return cluster_name.replace(".", " › ").replace("_", " ").title()

    def _create_chunked_dependency_diagrams(self, dependencies: Dict[str, Any]) -> str:
        """Generate an overview + per-cluster detail diagrams for large codebases."""
        clusters = self._cluster_modules(dependencies["modules"])
        ext_list = dependencies.get("external", [])

        # Assign a color to each cluster
        sorted_cluster_names = sorted(clusters.keys())
        cluster_color_map = {
            name: self.CLUSTER_COLORS[i % len(self.CLUSTER_COLORS)]
            for i, name in enumerate(sorted_cluster_names)
        }

        # ── OVERVIEW DIAGRAM ──────────────────────────────────────────
        overview = self._create_overview_diagram(clusters, cluster_color_map, dependencies, ext_list)

        # ── DETAIL DIAGRAMS ───────────────────────────────────────────
        details = []
        for cluster_name in sorted_cluster_names:
            modules = clusters[cluster_name]
            if len(modules) <= 1:
                continue  # Single-module clusters don't need a detail view
            detail = self._create_cluster_detail_diagram(
                cluster_name, modules, dependencies, cluster_color_map, ext_list
            )
            details.append((cluster_name, detail))

        # ── COMBINE ──────────────────────────────────────────────────
        parts = [
            "### 🔭 High-Level Overview",
            "",
            f"> *{len(clusters)} clusters identified — {len(dependencies['modules'])} total modules*",
            "",
            overview,
        ]
        for name, diagram in details:
            display = self._cluster_display_name(name)
            count = len(clusters[name])
            parts.append("")
            parts.append(f"### 🔍 {display} — {count} modules")
            parts.append("")
            parts.append(diagram)

        return "\n".join(parts)

    def _create_overview_diagram(self, clusters, cluster_color_map, dependencies, ext_list) -> str:
        """Generate a high-level overview with one node per cluster."""
        lines = ["```mermaid", self.THEME_CONFIG, "graph TD"]

        # One node per cluster
        cluster_ids = {}
        for cluster_name in sorted(clusters.keys()):
            safe_id = "c_" + cluster_name.replace(".", "_").replace(" ", "_")
            count = len(clusters[cluster_name])
            display = self._cluster_display_name(cluster_name)
            lines.append(f"    {safe_id}([{display}<br/>{count} modules])")
            cluster_ids[cluster_name] = safe_id

        # External deps summary node
        if ext_list:
            lines.append(f'    ext_deps[/"{len(ext_list)} External Packages"\\]')

        # Inter-cluster edges (deduplicated)
        cross_edges = set()
        ext_clusters = set()
        for from_mod, to_mod, _ in dependencies["edges"]:
            from_cluster = self._get_cluster_key(from_mod)
            if to_mod in ext_list:
                ext_clusters.add(from_cluster)
            else:
                to_cluster = self._get_cluster_key(to_mod)
                if from_cluster != to_cluster:
                    from_id = cluster_ids.get(from_cluster)
                    to_id = cluster_ids.get(to_cluster)
                    if from_id and to_id:
                        edge = (from_id, to_id)
                        if edge not in cross_edges:
                            lines.append(f"    {from_id} --> {to_id}")
                            cross_edges.add(edge)

        # External edges
        if ext_list:
            for cluster_name in sorted(ext_clusters):
                cid = cluster_ids.get(cluster_name)
                if cid:
                    lines.append(f"    {cid} -.-> ext_deps")

        # classDefs — each cluster gets its assigned color
        lines.append("")
        for cluster_name, color in cluster_color_map.items():
            safe_id = cluster_ids[cluster_name]
            lines.append(f"    classDef cls_{safe_id} fill:{color['fill']},stroke:{color['stroke']},stroke-width:2px,color:#fff,rx:12")
            lines.append(f"    class {safe_id} cls_{safe_id}")
        lines.append("    classDef extNode fill:#0d9488,stroke:#0f766e,stroke-width:2px,color:#fff,rx:8")
        if ext_list:
            lines.append("    class ext_deps extNode")

        # Link styles
        internal_edge_count = len(cross_edges)
        ext_edge_count = len(ext_clusters) if ext_list else 0
        if internal_edge_count > 0:
            indices = ",".join(str(i) for i in range(internal_edge_count))
            lines.append(f"    linkStyle {indices} stroke:#60a5fa,stroke-width:2px")
        if ext_edge_count > 0:
            ext_indices = ",".join(str(i) for i in range(internal_edge_count, internal_edge_count + ext_edge_count))
            lines.append(f"    linkStyle {ext_indices} stroke:#2dd4bf,stroke-width:1.5px,stroke-dasharray:5")

        lines.append("```")
        return "\n".join(lines)

    def _create_cluster_detail_diagram(self, cluster_name, modules, dependencies, cluster_color_map, ext_list) -> str:
        """Generate a focused diagram for a single cluster with cross-cluster stubs."""
        color = cluster_color_map.get(cluster_name, self.CLUSTER_COLORS[0])
        display = self._cluster_display_name(cluster_name)
        sg_id = "sg_" + cluster_name.replace(".", "_")

        lines = ["```mermaid", self.THEME_CONFIG, "graph TD"]

        # Cluster subgraph with internal modules
        lines.append(f"    subgraph {sg_id} [{display}]")
        lines.append("    direction TB")

        module_set = set(modules)
        for mod in sorted(modules):
            safe_id = mod.replace(".", "_")
            short_name = mod.split(".")[-1]
            lines.append(f"        {safe_id}([{short_name}])")
        lines.append("    end")

        # Internal edges (within this cluster) — deduplicated
        internal_edge_count = 0
        added_internal = set()
        cross_cluster_refs = set()
        for from_mod, to_mod, _ in dependencies["edges"]:
            if from_mod in module_set:
                from_id = from_mod.replace(".", "_")
                if to_mod in module_set:
                    to_id = to_mod.replace(".", "_")
                    edge_key = (from_id, to_id)
                    if from_id != to_id and edge_key not in added_internal:
                        lines.append(f"    {from_id} --> {to_id}")
                        added_internal.add(edge_key)
                        internal_edge_count += 1
                elif to_mod not in ext_list:
                    to_cluster = self._get_cluster_key(to_mod)
                    if to_cluster != cluster_name:
                        cross_cluster_refs.add(to_cluster)

        # Stub nodes for referenced external clusters
        cross_edge_count = 0
        if cross_cluster_refs:
            lines.append("")
            cross_edges_added = set()
            for ref_cluster in sorted(cross_cluster_refs):
                ref_id = "ref_" + ref_cluster.replace(".", "_")
                ref_display = self._cluster_display_name(ref_cluster)
                ref_color = cluster_color_map.get(ref_cluster, self.CLUSTER_COLORS[-1])
                lines.append(f"    {ref_id}[{ref_display}]")
                lines.append(f"    style {ref_id} fill:{ref_color['fill']},stroke:{ref_color['stroke']},stroke-width:2px,color:#fff,rx:8,stroke-dasharray:5")

            for from_mod, to_mod, _ in dependencies["edges"]:
                if from_mod in module_set and to_mod not in module_set and to_mod not in ext_list:
                    to_cluster = self._get_cluster_key(to_mod)
                    if to_cluster in cross_cluster_refs:
                        from_id = from_mod.replace(".", "_")
                        to_id = "ref_" + to_cluster.replace(".", "_")
                        edge_key = (from_id, to_id)
                        if edge_key not in cross_edges_added:
                            lines.append(f"    {from_id} -.-> {to_id}")
                            cross_edges_added.add(edge_key)
                            cross_edge_count += 1

        # classDefs
        lines.append("")
        lines.append(f"    classDef clusterNode fill:{color['fill']},stroke:{color['stroke']},stroke-width:2px,color:#fff,rx:10")
        for mod in modules:
            lines.append(f"    class {mod.replace('.', '_')} clusterNode")

        # Subgraph panel styling
        lines.append(f"    style {sg_id} fill:{color['fill']}22,stroke:{color['stroke']},stroke-width:2px,color:#e2e8f0,rx:12")

        # Link styles
        if internal_edge_count > 0:
            indices = ",".join(str(i) for i in range(internal_edge_count))
            lines.append(f"    linkStyle {indices} stroke:{color['stroke']},stroke-width:2px")
        if cross_edge_count > 0:
            cross_indices = ",".join(str(i) for i in range(internal_edge_count, internal_edge_count + cross_edge_count))
            lines.append(f"    linkStyle {cross_indices} stroke:#94a3b8,stroke-width:1.5px,stroke-dasharray:5")

        lines.append("```")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #                         FEATURE FLOW MAPPER                        #
    # ------------------------------------------------------------------ #

    async def generate_feature_flow(self, project_path: str, feature_name: Optional[str] = None, output_path: Optional[str] = None) -> Dict[str, Any]:
        try:
            target_path = Path(project_path).resolve()
            analysis = await self._analyze_features_with_ai(target_path, feature_name)
            mermaid_diagram = self._create_feature_flow_mermaid(analysis)
            markdown = self._format_feature_flow_output(mermaid_diagram, analysis, target_path)
            save_path = self._save_visualization(markdown, output_path, "feature-flow") if output_path else None
            
            return {
                "success": True, 
                "diagram_type": "feature_flow", 
                "markdown": markdown, 
                "mermaid": mermaid_diagram, 
                "saved_to": save_path, 
                "features_analyzed": len(analysis.get("features", []))
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to generate feature flow: {str(e)}"}

    async def _analyze_features_with_ai(self, target_path: Path, feature_name: Optional[str]) -> Dict[str, Any]:
        context = self._gather_project_context(target_path)
        prompt = build_feature_flow_prompt(
            project_name=target_path.name,
            structure=context["structure"],
            key_files=context["key_files"]
        )
        response = await self.watsonx.generate_text(prompt=prompt, max_tokens=2500, temperature=0.1)
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            return json.loads(json_match.group()) if json_match else self._create_basic_feature_analysis(target_path)
        except Exception:
            return self._create_basic_feature_analysis(target_path)

    def _create_feature_flow_mermaid(self, analysis: Dict[str, Any]) -> str:
        """Generate a clean sequence diagram using base theme for VS Code compatibility."""
        theme_config = (
            "%%{init: {'theme': 'base', 'themeVariables': {"
            " 'actorBkg': '#3b82f6',"
            " 'actorBorder': '#2563eb',"
            " 'actorTextColor': '#fff',"
            " 'actorLineColor': '#94a3b8',"
            " 'noteBkgColor': '#f1f5f9',"
            " 'noteTextColor': '#1e293b',"
            " 'noteBorderColor': '#3b82f6',"
            " 'activationBkgColor': '#dbeafe',"
            " 'activationBorderColor': '#60a5fa',"
            " 'signalColor': '#334155',"
            " 'signalTextColor': '#1e293b',"
            " 'fontFamily': 'Inter, Segoe UI, sans-serif'"
            "}}}%%"
        )
        lines = ["```mermaid", theme_config, "sequenceDiagram", "    autonumber"]
        participants = set()

        # 1. Collect all participant names
        for feature in analysis.get("features", []):
            for step in feature.get("flow_steps", []):
                participants.add(step.get("actor", "System"))
                participants.add(step.get("target", "System"))

        if not participants:
            participants.add("System")

        # 2. Map participants to safe alphanumeric IDs
        sorted_parts = sorted(participants)
        safe_map = {actor: f"p_{i}" for i, actor in enumerate(sorted_parts)}

        # 3. Declare participants — User gets an actor shape, others get regular
        for actor in sorted_parts:
            sid = safe_map[actor]
            if actor.lower() == "user":
                lines.append(f'    actor {sid} as User')
            else:
                # Shorten display: lib/qa_sentry/core.py -> qa_sentry/core
                short = actor.replace("lib/", "").replace(".py", "")
                lines.append(f'    participant {sid} as {short}')

        # 4. Feature workflow sections — deeper color rects
        feat_colors = [
            "rgb(59,130,246,0.15)",
            "rgb(139,92,246,0.15)",
            "rgb(236,72,153,0.12)",
            "rgb(16,185,129,0.12)"
        ]
        for idx, feature in enumerate(analysis.get("features", [])):
            color = feat_colors[idx % len(feat_colors)]
            feat_name = str(feature.get("name", "Feature")).replace(":", " -")

            lines.append("")
            lines.append(f"    rect {color}")
            lines.append(f"    Note right of {safe_map[sorted_parts[0]]}: {feat_name}")

            steps = feature.get("flow_steps", [])
            for step in steps:
                actor = safe_map.get(step.get("actor", "System"), "p_0")
                target = safe_map.get(step.get("target", "System"), "p_0")
                action = str(step.get("action", "process")).replace(":", " -")
                response = str(step.get("response", "done")).replace(":", " -")
                lines.append(f"    {actor}->>+{target}: {action}")
                lines.append(f"    {target}-->>-{actor}: {response}")

            lines.append("    end")

        lines.append("```")
        return "\n".join(lines)
# ------------------------------------------------------------------ #
    #                     PROJECT CONCEPT VISUALIZER                     #
    # ------------------------------------------------------------------ #

    async def generate_project_concept(self, project_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        try:
            target_path = Path(project_path).resolve()
            concept = await self._analyze_project_concept_with_ai(target_path)
            mermaid_diagram = self._create_concept_mermaid(concept)
            markdown = self._format_concept_output(mermaid_diagram, concept, target_path)
            
            # Saves the .md file
            save_path = self._save_visualization(markdown, output_path, "project-concept") if output_path else None
            
            return {
                "success": True, 
                "diagram_type": "project_concept", 
                "markdown": markdown, 
                "mermaid": mermaid_diagram, 
                "saved_to": save_path,
                "components": len(concept.get("components", []))
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to generate project concept: {str(e)}"}

    async def _analyze_project_concept_with_ai(self, target_path: Path) -> Dict[str, Any]:
        context = self._gather_project_context(target_path)
        prompt = build_project_concept_prompt(
            project_name=target_path.name,
            structure=context["structure"]
        )
        response = await self.watsonx.generate_text(prompt=prompt, max_tokens=1500, temperature=0.2)
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            return json.loads(json_match.group()) if json_match else self._create_basic_concept(target_path)
        except Exception:
            return self._create_basic_concept(target_path)

    def _create_concept_mermaid(self, concept: Dict[str, Any]) -> str:
        """Generate a clean concept map using base theme for VS Code compatibility."""
        theme_config = (
            "%%{init: {'theme': 'base', 'themeVariables': {"
            " 'fontFamily': 'Inter, Segoe UI, sans-serif'"
            "}}}%%"
        )
        lines = ["```mermaid", theme_config, "graph LR"]

        # Class definitions — vibrant fills on dark background
        lines.append("    classDef ui fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef server fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef engine fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef database fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff,rx:10")
        lines.append("    classDef external fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff,rx:8")
        lines.append("    classDef defaultNode fill:#64748b,stroke:#475569,stroke-width:2px,color:#fff,rx:10")
        lines.append("")

        # Internal components subgraph
        components = [c for c in concept.get("components", []) if isinstance(c, dict)]
        if components:
            lines.append("    subgraph core [System Architecture]")
            lines.append("    direction TB")

            for comp in components:
                comp_name = str(comp.get("name", "Unknown"))
                comp_id = comp_name.replace(" ", "_").replace(".", "_").replace("/", "_")
                comp_type = str(comp.get("type", "component")).lower()

                # Node shape and class based on type — no emoji
                if any(k in comp_type for k in ("database", "db", "storage")):
                    lines.append(f"        {comp_id}[({comp_name})]")
                    lines.append(f"        class {comp_id} database")
                elif any(k in comp_type for k in ("ui", "frontend", "client")):
                    lines.append(f"        {comp_id}[/{comp_name}\\]")
                    lines.append(f"        class {comp_id} ui")
                elif any(k in comp_type for k in ("engine", "core", "processor")):
                    lines.append(f"        {comp_id}([{comp_name}])")
                    lines.append(f"        class {comp_id} engine")
                elif any(k in comp_type for k in ("server", "api", "backend")):
                    lines.append(f"        {comp_id}([{comp_name}])")
                    lines.append(f"        class {comp_id} server")
                else:
                    lines.append(f"        {comp_id}([{comp_name}])")
                    lines.append(f"        class {comp_id} defaultNode")

            lines.append("    end")
            lines.append("")

        # Connection edges — thick arrows, no labels
        edge_count = 0
        for comp in components:
            comp_name = str(comp.get("name", "Unknown"))
            comp_id = comp_name.replace(" ", "_").replace(".", "_").replace("/", "_")
            for target in comp.get("connects_to", []):
                if isinstance(target, dict):
                    target = str(target.get("name", target.get("target", "Unknown")))
                target_id = str(target).replace(" ", "_").replace(".", "_").replace("/", "_")
                lines.append(f"    {comp_id} ==> {target_id}")
                edge_count += 1

        # External services subgraph
        ext_services = concept.get("external_services", [])
        if ext_services:
            lines.append("")
            lines.append("    subgraph ext [External Services]")
            lines.append("    direction TB")
            for service in ext_services:
                if isinstance(service, dict):
                    service = str(service.get("name", service.get("service", "External")))
                service_str = str(service)
                safe_id = service_str.replace(" ", "_").replace(".", "_").replace("/", "_")
                lines.append(f"        ext_{safe_id}{{{{{service_str}}}}}")
                lines.append(f"        class ext_{safe_id} external")
            lines.append("    end")

        # Subgraph styling — dark panels
        lines.append("")
        lines.append("    style core fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0,rx:12")
        if ext_services:
            lines.append("    style ext fill:#1c1917,stroke:#ef4444,stroke-width:2px,color:#e2e8f0,rx:12")

        # Link styles — thick colored arrows
        if edge_count > 0:
            indices = ",".join(str(i) for i in range(edge_count))
            lines.append(f"    linkStyle {indices} stroke:#60a5fa,stroke-width:3px")

        lines.append("```")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #                       MARKDOWN FORMATTERS                          #
    # ------------------------------------------------------------------ #

    def _format_dependency_output(self, mermaid: str, dependencies: Dict[str, Any], target_path: Path) -> str:
        total_mods = len(dependencies["modules"])
        total_deps = len(dependencies["edges"])
        total_ext = len(dependencies["external"])
        is_chunked = total_mods > self.MAX_DIAGRAM_NODES

        # Group modules by layer
        layers = defaultdict(list)
        for mod in sorted(dependencies["modules"].keys()):
            root = mod.split('.')[0] if '.' in mod else "root"
            layers[root].append(mod)

        parts = [
            f"# 📦 Dependency Chain — `{target_path.name}`",
            f"> Generated: {get_timestamp()}",
            "",
            "## 📊 Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Modules | **{total_mods}** |",
            f"| Internal Dependencies | **{total_deps - total_ext}** |",
            f"| External Packages | **{total_ext}** |",
            f"| Architecture Layers | **{len(layers)}** |",
        ]

        if is_chunked:
            clusters = self._cluster_modules(dependencies["modules"])
            parts.append(f"| Diagram Sections | **{len(clusters) + 1}** (1 overview + {len(clusters)} details) |")

        parts.extend([
            "",
            "## 🏗️ Architecture Diagram",
            "",
            mermaid,
            "",
            "## 🎨 Legend",
            "",
        ])

        if is_chunked:
            # Dynamic legend based on cluster colors
            clusters = self._cluster_modules(dependencies["modules"])
            sorted_names = sorted(clusters.keys())
            parts.append("| Color | Cluster | Modules |")
            parts.append("|-------|---------|---------|")
            for i, name in enumerate(sorted_names):
                color = self.CLUSTER_COLORS[i % len(self.CLUSTER_COLORS)]
                display = self._cluster_display_name(name)
                count = len(clusters[name])
                parts.append(f"| {color['label']} | {display} | {count} |")
            parts.append(f"| Teal | External packages | {total_ext} |")
            parts.append(f"| ⬜ Dashed border | Cross-cluster reference (stub) | — |")
        else:
            parts.append("| Color | Layer |")
            parts.append("|-------|-------|")
            parts.append("| 🔵 Blue | Core entry points |")
            parts.append("| 🟣 Purple | Library modules |")
            parts.append("| 🟠 Orange | Test suites |")
            parts.append("| 🟢 Teal | External packages |")

        parts.append("")
        parts.append("## 📁 Module Reference")
        parts.append("")
        parts.append("| Module | Source Path |")
        parts.append("|--------|------------|")
        for m, p in sorted(dependencies["modules"].items()):
            parts.append(f"| `{m}` | `{p}` |")

        parts.append("")
        parts.append("---")
        parts.append("*Made with IBM Bob — BobSuite Visualizer Engine*")
        return "\n".join(parts)

    def _format_feature_flow_output(self, mermaid: str, analysis: Dict[str, Any], target_path: Path) -> str:
        features = analysis.get("features", [])
        parts = [
            f"# 🔄 Feature Flow Map — `{target_path.name}`",
            f"> Generated: {get_timestamp()}",
            "",
            "## 📊 Summary",
            "",
            f"**Features Analyzed:** {len(features)}",
            "",
            "## 🔀 Execution Sequence",
            "",
            mermaid,
            "",
            "## 📋 Feature Details",
            "",
        ]
        for i, f in enumerate(features, 1):
            name = f.get("name", "N/A")
            desc = f.get("description", "N/A")
            entry = f.get("entry_point", "N/A")
            steps = len(f.get("flow_steps", []))
            parts.append(f"### {i}. {name}")
            parts.append(f"- **Description:** {desc}")
            parts.append(f"- **Entry Point:** `{entry}`")
            parts.append(f"- **Flow Steps:** {steps}")
            parts.append("")

        parts.append("---")
        parts.append("*Made with IBM Bob — BobSuite Visualizer Engine*")
        return "\n".join(parts)

    def _format_concept_output(self, mermaid: str, concept: Dict[str, Any], target_path: Path) -> str:
        components = [c for c in concept.get("components", []) if isinstance(c, dict)]
        ext_services = concept.get("external_services", [])
        parts = [
            f"# 🗺️ Project Concept Map — `{target_path.name}`",
            "",
            "## 📝 Overview",
            "",
            concept.get("description", "No description available."),
            "",
            "## 📊 Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Components | **{len(components)}** |",
            f"| External Services | **{len(ext_services)}** |",
            f"| Project Type | **{concept.get('project_type', 'N/A')}** |",
            "",
            "## 🏗️ Architecture Blueprint",
            "",
            mermaid,
            "",
            "## 🧩 Component Details",
            "",
            "| Component | Type | Description |",
            "|-----------|------|-------------|",
        ]
        for comp in components:
            name = comp.get("name", "Unknown")
            ctype = comp.get("type", "component")
            desc = str(comp.get("description", "—"))[:80]
            parts.append(f"| **{name}** | `{ctype}` | {desc} |")

        if ext_services:
            parts.append("")
            parts.append("## 🌐 External Services")
            parts.append("")
            for svc in ext_services:
                if isinstance(svc, dict):
                    svc = svc.get("name", svc.get("service", "External"))
                parts.append(f"- 🔗 **{svc}**")

        parts.append("")
        parts.append("---")
        parts.append("*Made with IBM Bob — BobSuite Visualizer Engine*")
        return "\n".join(parts)

    def _gather_project_context(self, target_path: Path) -> Dict[str, str]:
        structure_lines = []
        key_files_content = {}
        for item in sorted(target_path.rglob("*")):
            if any(skip in item.parts for skip in ["__pycache__", "venv", ".venv", ".git", "node_modules"]): continue
            if item.is_file(): structure_lines.append(f"  {item.relative_to(target_path)}")
                
        for pattern in ["README.md", "main.py", "app.py", "server.py", "manage.py"]:
            for match in list(target_path.rglob(pattern))[:1]:
                content = self._get_file_content(str(match))
                if content: key_files_content[str(match.relative_to(target_path))] = content[:750]
                    
        return {"structure": "\n".join(structure_lines[:60]), "key_files": "\n\n".join([f"=== File: {k} ===\n{v}" for k, v in key_files_content.items()])}

    def _create_basic_feature_analysis(self, target_path: Path) -> Dict[str, Any]:
        return {"features": [{"name": "Default Init Core", "description": "Fallback automation module analysis", "entry_point": "main.py", "flow_steps": []}]}

    def _create_basic_concept(self, target_path: Path) -> Dict[str, Any]:
        return {"project_type": "Python application package", "description": "System architecture codebase", "components": [{"name": "AppCore", "type": "server", "description": "Primary internal services processor backend Layer", "connects_to": []}], "external_services": []}

    def _save_visualization(self, markdown: str, output_path: str, diagram_type: str) -> str:
        out = Path(output_path)
        if out.is_dir() or not out.suffix: out = out / f"{diagram_type}_{get_timestamp().replace(':', '-').replace(' ', '_')}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f: f.write(markdown)
        return str(out)


# Made with Bob