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

    def _create_dependency_mermaid(self, dependencies: Dict[str, Any]) -> str:
        # Color palette for layer subgraphs
        layer_colors = {
            "Root": {"fill": "#f8fafc", "stroke": "#cbd5e1", "text": "#334155"},
            "lib": {"fill": "#f1f5f9", "stroke": "#94a3b8", "text": "#334155"},
            "tests": {"fill": "#fdf2f8", "stroke": "#fbcfe8", "text": "#831843"},
            "dataset_bob": {"fill": "#f0fdf4", "stroke": "#bbf7d0", "text": "#166534"},
        }
        default_layer = {"fill": "#ffffff", "stroke": "#e2e8f0", "text": "#1e293b"}

        lines = ["```mermaid", "%%{init: {'theme': 'default', 'themeVariables': { 'background': '#ffffff'}}}%%", "graph TD"]

        # Subgraph grouping
        subgraphs = defaultdict(list)
        for module_name in dependencies["modules"].keys():
            root_part = module_name.split('.')[0] if '.' in module_name else "Root"
            subgraphs[root_part].append(module_name)

        for group, elements in subgraphs.items():
            label = group.upper().replace("_", " ")
            lines.append(f"    subgraph {group} [🔹 {label}]")
            lines.append(f"    direction TB")
            for mod in elements:
                safe_id = mod.replace(".", "_")
                display_name = mod.split(".")[-1]
                lines.append(f"        {safe_id}([🧩 {display_name}])")
            lines.append("    end")

        if dependencies["external"]:
            lines.append("    subgraph External [📦 EXTERNAL PACKAGES]")
            lines.append("    direction TB")
            for ext in dependencies["external"]:
                safe_id = f"ext_{ext.replace('.', '_')}"
                lines.append(f"        {safe_id}[/{ext}\\]")
            lines.append("    end")

        # Styled edges
        added_edges = set()
        for from_mod, to_mod, imp_type in dependencies["edges"]:
            from_id = from_mod.replace(".", "_")
            if to_mod in dependencies["external"]:
                to_id = f"ext_{to_mod.replace('.', '_')}"
                style = "-.->|uses|"
            else:
                to_id = to_mod.replace(".", "_")
                style = "-->|imports|"

            edge_key = (from_id, to_id)
            if edge_key not in added_edges and from_id != to_id:
                lines.append(f"    {from_id} {style} {to_id}")
                added_edges.add(edge_key)

        # Apply styles via classDefs
        lines.append("")
        lines.append("    classDef coreNode fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#fff,rx:12")
        lines.append("    classDef libNode fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,rx:12")
        lines.append("    classDef testNode fill:#ec4899,stroke:#be185d,stroke-width:2px,color:#fff,rx:12")
        lines.append("    classDef extNode fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,rx:8")

        for group, elements in subgraphs.items():
            cls = "coreNode" if group == "Root" else "testNode" if group == "tests" else "libNode"
            for mod in elements:
                safe_id = mod.replace(".", "_")
                lines.append(f"    class {safe_id} {cls}")

        if dependencies["external"]:
            for ext in dependencies["external"]:
                safe_id = f"ext_{ext.replace('.', '_')}"
                lines.append(f"    class {safe_id} extNode")

        # Subgraph styling
        lines.append("")
        for group in subgraphs.keys():
            c = layer_colors.get(group, default_layer)
            lines.append(f"    style {group} fill:{c['fill']},stroke:{c['stroke']},stroke-width:2px,color:{c['text']},rx:16")
        if dependencies["external"]:
            lines.append("    style External fill:#f0fdfa,stroke:#a7f3d0,stroke-width:2px,color:#065f46,rx:16")

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
        lines = ["```mermaid", "%%{init: {'theme': 'default', 'themeVariables': { 'background': '#ffffff'}}}%%", "sequenceDiagram", "    autonumber"]
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
                lines.append(f'    actor {sid} as 👤 {actor}')
            else:
                # Shorten display: lib/qa_sentry/core.py → qa_sentry/core
                short = actor.replace("lib/", "").replace(".py", "")
                lines.append(f'    participant {sid} as {short}')

        # 4. Feature workflow sections
        feat_colors = ["rgb(59,130,246,0.1)", "rgb(139,92,246,0.1)", "rgb(236,72,153,0.1)", "rgb(16,185,129,0.1)"]
        for idx, feature in enumerate(analysis.get("features", [])):
            color = feat_colors[idx % len(feat_colors)]
            feat_name = str(feature.get("name", "Feature")).replace(":", " -")
            clean_desc = str(feature.get("description", "")).replace("\n", " ").replace(":", " -")[:80]

            lines.append(f"")
            lines.append(f"    rect {color}")
            lines.append(f"    Note right of {safe_map[sorted_parts[0]]}: 🔷 {feat_name}")

            steps = feature.get("flow_steps", [])
            for i, step in enumerate(steps):
                actor = safe_map.get(step.get("actor", "System"), "p_0")
                target = safe_map.get(step.get("target", "System"), "p_0")
                action = str(step.get("action", "process")).replace(":", " -")
                # Use a meaningful return instead of generic "Status Confirm"
                response = str(step.get("response", "✓ done")).replace(":", " -")
                lines.append(f"    {actor}->>+{target}: {action}")
                lines.append(f"    {target}-->>-{actor}: {response}")

            lines.append(f"    end")

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
        lines = ["```mermaid", "%%{init: {'theme': 'default', 'themeVariables': { 'background': '#ffffff'}}}%%", "graph LR"]

        # Rich class definitions with gradients and rounded corners
        lines.append("    classDef ui fill:#3b82f6,stroke:#1d4ed8,stroke-width:3px,color:#fff,rx:12")
        lines.append("    classDef server fill:#8b5cf6,stroke:#6d28d9,stroke-width:3px,color:#fff,rx:12")
        lines.append("    classDef engine fill:#f59e0b,stroke:#d97706,stroke-width:3px,color:#fff,rx:12")
        lines.append("    classDef database fill:#10b981,stroke:#047857,stroke-width:3px,color:#fff,rx:12")
        lines.append("    classDef external fill:#ef4444,stroke:#b91c1c,stroke-width:2px,color:#fff,rx:8")
        lines.append("")

        # Type → emoji mapping
        type_emoji = {
            "database": "🗄️", "db": "🗄️", "storage": "🗄️",
            "ui": "🖥️", "frontend": "🖥️", "client": "🖥️",
            "server": "⚙️", "api": "⚙️", "backend": "⚙️",
            "engine": "🔥", "core": "🔥", "processor": "🔥",
        }

        # Internal components subgraph
        components = [c for c in concept.get("components", []) if isinstance(c, dict)]
        if components:
            lines.append("    subgraph core [🏗️ System Architecture]")
            lines.append("    direction TB")

            for comp in components:
                comp_name = str(comp.get("name", "Unknown"))
                comp_id = comp_name.replace(" ", "_").replace(".", "_").replace("/", "_")
                comp_type = str(comp.get("type", "component")).lower()
                desc = str(comp.get("description", ""))[:50]

                # Pick emoji based on type keywords
                emoji = "📦"
                for key, em in type_emoji.items():
                    if key in comp_type:
                        emoji = em
                        break

                # Node shape based on type
                if any(k in comp_type for k in ("database", "db", "storage")):
                    lines.append(f"        {comp_id}[({emoji} {comp_name})]")
                    lines.append(f"        class {comp_id} database")
                elif any(k in comp_type for k in ("ui", "frontend", "client")):
                    lines.append(f"        {comp_id}[/{emoji} {comp_name}\\]")
                    lines.append(f"        class {comp_id} ui")
                elif any(k in comp_type for k in ("engine", "core", "processor")):
                    lines.append(f"        {comp_id}([{emoji} {comp_name}])")
                    lines.append(f"        class {comp_id} engine")
                else:
                    lines.append(f"        {comp_id}([{emoji} {comp_name}])")
                    if any(k in comp_type for k in ("server", "api", "backend")):
                        lines.append(f"        class {comp_id} server")

            lines.append("    end")
            lines.append("")

        # Connection edges with thick styled arrows
        for comp in components:
            comp_name = str(comp.get("name", "Unknown"))
            comp_id = comp_name.replace(" ", "_").replace(".", "_").replace("/", "_")
            for target in comp.get("connects_to", []):
                if isinstance(target, dict):
                    target = str(target.get("name", target.get("target", "Unknown")))
                target_id = str(target).replace(" ", "_").replace(".", "_").replace("/", "_")
                lines.append(f"    {comp_id} ==>|connects| {target_id}")

        # External services subgraph
        ext_services = concept.get("external_services", [])
        if ext_services:
            lines.append("")
            lines.append("    subgraph ext [🌐 External Services]")
            lines.append("    direction TB")
            for service in ext_services:
                if isinstance(service, dict):
                    service = str(service.get("name", service.get("service", "External")))
                service_str = str(service)
                safe_id = service_str.replace(" ", "_").replace(".", "_").replace("/", "_")
                lines.append(f"        ext_{safe_id}{{{{🔗 {service_str}}}}}")
                lines.append(f"        class ext_{safe_id} external")
            lines.append("    end")

        # Subgraph styling
        lines.append("")
        lines.append("    style core fill:#f8fafc,stroke:#94a3b8,stroke-width:2px,color:#334155,rx:16")
        if ext_services:
            lines.append("    style ext fill:#fef2f2,stroke:#fca5a5,stroke-width:2px,color:#991b1b,rx:16")

        lines.append("```")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #                       MARKDOWN FORMATTERS                          #
    # ------------------------------------------------------------------ #

    def _format_dependency_output(self, mermaid: str, dependencies: Dict[str, Any], target_path: Path) -> str:
        total_mods = len(dependencies["modules"])
        total_deps = len(dependencies["edges"])
        total_ext = len(dependencies["external"])

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
            "",
            "## 🏗️ Architecture Diagram",
            "",
            mermaid,
            "",
            "## 🎨 Legend",
            "",
            "| Color | Layer |",
            "|-------|-------|",
            "| 🔵 Blue | Core entry points |",
            "| 🟣 Purple | Library modules |",
            "| 🩷 Pink | Test suites |",
            "| 🟢 Green | External packages |",
            "",
            "## 📁 Module Reference",
            "",
            "| Module | Source Path |",
            "|--------|------------|",
        ]
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