"""
BobSuite Master Test Runner
Runs all unit tests (offline) and integration tests (API) in one go
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ------------------------------------------------------------------ #
#                       IMPORTS                                        #
# ------------------------------------------------------------------ #

from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.qa_sentry.parsers import sanitize_json, validate_json_schema
from lib.qa_sentry.auto_fixer import validate_python_syntax
from lib.qa_sentry.git_utils import parse_diff_hunks
from lib.autodocs import AutoDocs
from lib.ideation import IdeationEngine
from lib.visualizer import VisualizerEngine


# ------------------------------------------------------------------ #
#                       HELPERS                                        #
# ------------------------------------------------------------------ #

RESULTS = {}


def section(title):
    print(f"\n{'=' * 65}")
    print(f"  {title}")
    print(f"{'=' * 65}\n")


def record(suite, test_name, passed, detail=""):
    icon = "PASS" if passed else "FAIL"
    print(f"  [{icon}] {test_name}")
    if detail:
        print(f"         {detail}")
    RESULTS.setdefault(suite, []).append(passed)


# ------------------------------------------------------------------ #
#                   1. PARSER UNIT TESTS                               #
# ------------------------------------------------------------------ #

def test_parsers():
    section("1. QA Sentry Parsers")

    # 1a: markdown wrapper
    raw = '```json\n{"summary": {"health_score": 80, "risk_level": "LOW", "executive_summary": "clean"}, "findings": []}\n```'
    try:
        data = json.loads(sanitize_json(raw))
        record("parsers", "Markdown wrapper stripping", validate_json_schema(data))
    except Exception as e:
        record("parsers", "Markdown wrapper stripping", False, str(e))

    # 1b: conversational prefix
    raw2 = 'Here is my analysis:\n{"summary": {"health_score": 50, "risk_level": "MEDIUM", "executive_summary": "issues"}, "findings": []}'
    try:
        data2 = json.loads(sanitize_json(raw2))
        record("parsers", "Conversational prefix removal", validate_json_schema(data2))
    except Exception as e:
        record("parsers", "Conversational prefix removal", False, str(e))

    # 1c: trailing text
    raw3 = '{"summary": {"health_score": 90, "risk_level": "LOW", "executive_summary": "good"}, "findings": []} Hope this helps!'
    try:
        data3 = json.loads(sanitize_json(raw3))
        record("parsers", "Trailing text removal", validate_json_schema(data3))
    except Exception as e:
        record("parsers", "Trailing text removal", False, str(e))

    # 1d: invalid schema
    invalid = {"summary": {"health_score": 50}, "findings": []}
    record("parsers", "Invalid schema rejected", not validate_json_schema(invalid))

    # 1e: valid finding schema (with solution_explanation)
    valid = {
        "summary": {"health_score": 70, "risk_level": "MEDIUM", "executive_summary": "test"},
        "findings": [{
            "id": "SEC-001", "category": "SECURITY", "severity": "HIGH",
            "line_numbers": [1], "title": "test", "deep_dive": "test",
            "solution_explanation": "test", "reference": "CWE-89", "fix_code_snippet": "fix"
        }]
    }
    record("parsers", "Valid schema with solution_explanation accepted", validate_json_schema(valid))


# ------------------------------------------------------------------ #
#                   2. AUTO-FIXER UNIT TESTS                           #
# ------------------------------------------------------------------ #

def test_auto_fixer():
    section("2. Auto Fixer (AST Validation)")
    record("auto_fixer", "Valid Python accepted", validate_python_syntax("x = 1\nprint(x)"))
    record("auto_fixer", "Invalid Python rejected", not validate_python_syntax("def broken(\n  x ="))
    record("auto_fixer", "Empty string accepted", validate_python_syntax(""))


# ------------------------------------------------------------------ #
#                   3. GIT UTILS UNIT TESTS                            #
# ------------------------------------------------------------------ #

def test_git_utils():
    section("3. Git Utils (Diff Parsing)")

    diff = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -10,5 +10,8 @@
 some code
+new line 1
"""
    files = parse_diff_hunks(diff)
    record("git_utils", "Standard diff parsing", len(files) == 1 and 10 in files[0]['changed_lines'])

    multi = """diff --git a/a.py b/a.py
--- a/a.py
+++ b/a.py
@@ -1,3 +1,5 @@
diff --git a/b.js b/b.js
--- a/b.js
+++ b/b.js
@@ -20,4 +20,6 @@
"""
    record("git_utils", "Multi-file diff parsing", len(parse_diff_hunks(multi)) == 2)
    record("git_utils", "Empty diff handling", len(parse_diff_hunks("")) == 0)


# ------------------------------------------------------------------ #
#                   4. IMPORT CHAIN VERIFICATION                       #
# ------------------------------------------------------------------ #

def test_imports():
    section("4. Import Chain Verification")
    chains = [
        ("lib.utils", "from lib.utils import detect_language, read_file_safe, get_timestamp, format_markdown_header, SUPPORTED_EXTENSIONS"),
        ("lib.utils.constants", "from lib.utils.constants import SUPPORTED_EXTENSIONS"),
        ("lib.utils.file_io", "from lib.utils.file_io import read_file_safe, detect_language"),
        ("lib.utils.formatting", "from lib.utils.formatting import get_timestamp, format_markdown_header"),
        ("lib.utils.cache", "from lib.utils.cache import get_cache"),
        ("lib.qa_sentry", "from lib.qa_sentry import QASentry"),
        ("lib.qa_sentry.core", "from lib.qa_sentry.core import QASentry"),
        ("lib.qa_sentry.parsers", "from lib.qa_sentry.parsers import sanitize_json, validate_json_schema"),
        ("lib.qa_sentry.auto_fixer", "from lib.qa_sentry.auto_fixer import apply_auto_fixes, validate_python_syntax"),
        ("lib.qa_sentry.git_utils", "from lib.qa_sentry.git_utils import parse_diff_hunks"),
        ("lib.qa_sentry.prompts", "from lib.qa_sentry.prompts import build_finder_prompt, build_critic_prompt"),
        ("lib.autodocs", "from lib.autodocs import AutoDocs"),
        ("lib.autodocs.core", "from lib.autodocs.core import AutoDocs"),
        ("lib.autodocs.prompts", "from lib.autodocs.prompts import get_documentation_prompt"),
        ("lib.ideation", "from lib.ideation import IdeationEngine"),
        ("lib.ideation.core", "from lib.ideation.core import IdeationEngine"),
        ("lib.ideation.prompts", "from lib.ideation.prompts import build_prd_synthesis_prompt"),
        ("lib.visualizer", "from lib.visualizer import VisualizerEngine"),
        ("lib.visualizer.core", "from lib.visualizer.core import VisualizerEngine"),
        ("lib.visualizer.prompts", "from lib.visualizer.prompts import build_feature_flow_prompt"),
    ]
    for name, stmt in chains:
        try:
            exec(stmt)
            record("imports", name, True)
        except Exception as e:
            record("imports", name, False, str(e))


# ------------------------------------------------------------------ #
#               5. REVIEWER.TXT SCHEMA CONSISTENCY                     #
# ------------------------------------------------------------------ #

def test_reviewer_schema():
    section("5. Reviewer Prompt Schema Consistency")

    reviewer_path = Path(__file__).parent.parent / "lib" / "qa_sentry" / "reviewer.txt"
    record("schema", "reviewer.txt exists", reviewer_path.exists())

    if reviewer_path.exists():
        content = reviewer_path.read_text(encoding="utf-8")
        record("schema", "Contains solution_explanation in examples",
               "solution_explanation" in content)
        record("schema", "Contains deep_dive in examples",
               "deep_dive" in content)
        record("schema", "Contains fix_code_snippet in examples",
               "fix_code_snippet" in content)
        record("schema", "Contains reference in examples",
               "reference" in content)

        # Verify all 3 few-shot examples contain solution_explanation
        count = content.count('"solution_explanation"')
        record("schema", f"All 3 examples have solution_explanation (found {count})", count >= 3)

    test_persona_path = Path(__file__).parent.parent / "lib" / "qa_sentry" / "test_persona.txt"
    record("schema", "test_persona.txt exists", test_persona_path.exists())
    if test_persona_path.exists():
        content = test_persona_path.read_text(encoding="utf-8")
        record("schema", "Contains SDET Vanguard Bob", "SDET Vanguard Bob" in content)
        record("schema", "Contains S/S/R Naming Convention", "S/S/R Naming Convention" in content)



# ------------------------------------------------------------------ #
#               6. INTEGRATION: QA SENTRY LIVE SCAN                    #
# ------------------------------------------------------------------ #

async def test_qa_sentry_live():
    section("6. QA Sentry Live Scan (Watsonx API)")
    try:
        client = WatsonxClient()
        sentry = QASentry(client)

        dataset = Path(__file__).parent.parent.parent / "dataset_balancia"
        target = dataset / "src" / "app" / "actions.ts"
        if not target.exists():
            ts = list(dataset.rglob("*.ts"))
            if not ts:
                record("qa_live", "Balancia scan", True, "SKIP - no .ts files")
                return
            target = ts[0]

        print(f"  Scanning: {target.name} ({target.stat().st_size} bytes)")
        print(f"  Running Finder -> Critic pipeline...")

        result = await sentry.scan_code(str(target))
        passed = result.get("success", False)
        summary = result.get("summary", {})
        record("qa_live", "Scan completed", passed,
               f"Score: {summary.get('health_score', '?')} | Risk: {summary.get('risk_level', '?')} | Findings: {len(result.get('findings', []))}")
    except Exception as e:
        record("qa_live", "Scan completed", False, str(e))


# ------------------------------------------------------------------ #
#               7. INTEGRATION: AUTODOCS LIVE                          #
# ------------------------------------------------------------------ #

async def test_autodocs_live():
    section("7. AutoDocs Live Generation (Watsonx API)")
    try:
        client = WatsonxClient()
        autodocs = AutoDocs(client)

        dataset = Path(__file__).parent.parent.parent / "dataset_balancia"
        target = dataset / "src" / "lib" / "ilmu.ts"
        if not target.exists():
            ts = list(dataset.rglob("*.ts"))
            target = ts[0] if ts else None
        if not target:
            record("autodocs_live", "Doc generation", True, "SKIP - no files")
            return

        print(f"  Documenting: {target.name}")
        result = await autodocs.generate_docs(str(target), "api")
        passed = len(result) > 100 and "Error" not in result[:50]
        record("autodocs_live", "API doc generation", passed, f"{len(result)} chars generated")
    except Exception as e:
        record("autodocs_live", "API doc generation", False, str(e))


# ------------------------------------------------------------------ #
#               8. INTEGRATION: VISUALIZER LIVE                        #
# ------------------------------------------------------------------ #

async def test_visualizer_live():
    section("8. Visualizer Live (Dependency Chain)")
    try:
        client = WatsonxClient()
        viz = VisualizerEngine(client)
        project = str(Path(__file__).parent.parent)

        result = await viz.generate_dependency_chain(project_path=project, max_depth=2)
        passed = result.get("success", False)
        stats = result.get("stats", {})
        record("visualizer_live", "Dependency chain", passed,
               f"Modules: {stats.get('total_modules', '?')} | Deps: {stats.get('total_dependencies', '?')}")
    except Exception as e:
        record("visualizer_live", "Dependency chain", False, str(e))


# ------------------------------------------------------------------ #
#               9. INTEGRATION: IDEATION                               #
# ------------------------------------------------------------------ #

async def test_ideation_live():
    section("9. Ideation Framework (No API call)")
    try:
        client = WatsonxClient()
        engine = IdeationEngine(client)
        framework = engine.get_framework(include_examples=True)
        passed = framework is not None and len(framework.get("pillars", {})) > 0
        record("ideation_live", "Framework retrieval", passed,
               f"{len(framework.get('pillars', {}))} pillars loaded")
    except Exception as e:
        record("ideation_live", "Framework retrieval", False, str(e))


# ------------------------------------------------------------------ #
#                       MAIN RUNNER                                    #
# ------------------------------------------------------------------ #

def main():
    print("\n" + "=" * 65)
    print("  BOBSUITE MASTER TEST SUITE")
    print("  All engines — Unit + Integration")
    print("=" * 65)

    # --- Unit Tests (no API calls) ---
    test_parsers()
    test_auto_fixer()
    test_git_utils()
    test_imports()
    test_reviewer_schema()

    # --- Integration Tests (Watsonx API) ---
    print(f"\n{'=' * 65}")
    print("  INTEGRATION TESTS (requires Watsonx API)")
    print(f"{'=' * 65}")

    asyncio.run(test_qa_sentry_live())
    asyncio.run(test_autodocs_live())
    asyncio.run(test_visualizer_live())
    asyncio.run(test_ideation_live())

    # --- Final Summary ---
    section("FINAL RESULTS")
    total_pass = 0
    total_fail = 0
    for suite, results_list in RESULTS.items():
        p = sum(results_list)
        f = len(results_list) - p
        total_pass += p
        total_fail += f
        icon = "OK" if f == 0 else "XX"
        print(f"  [{icon}] {suite}: {p}/{len(results_list)} passed")

    print(f"\n  TOTAL: {total_pass}/{total_pass + total_fail} passed")
    if total_fail == 0:
        print("\n  ALL TESTS PASSED!")
    else:
        print(f"\n  {total_fail} TEST(S) FAILED - review output above")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
