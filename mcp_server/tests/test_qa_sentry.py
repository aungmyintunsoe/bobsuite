"""
QA Sentry Integration Test Suite
Tests all refactored modules against the real dataset_balancia codebase
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from watsonx_client import WatsonxClient
from lib.qa_sentry import QASentry
from lib.qa_sentry.parsers import sanitize_json, validate_json_schema
from lib.qa_sentry.auto_fixer import validate_python_syntax
from lib.qa_sentry.git_utils import parse_diff_hunks


# ------------------------------------------------------------------ #
#                       UNIT TESTS                                     #
# ------------------------------------------------------------------ #

def test_parsers():
    """Test JSON sanitization and schema validation (no API calls needed)"""
    print("=" * 60)
    print("TEST 1: Parsers (sanitize_json + validate_json_schema)")
    print("=" * 60)
    passed = 0
    failed = 0

    # Test 1a: Strip markdown wrappers
    raw = '```json\n{"summary": {"health_score": 80, "risk_level": "LOW", "executive_summary": "clean"}, "findings": []}\n```'
    cleaned = sanitize_json(raw)
    try:
        data = json.loads(cleaned)
        assert validate_json_schema(data), "Schema validation failed"
        print("  [PASS] 1a: Markdown wrapper stripping")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] 1a: Markdown wrapper stripping - {e}")
        failed += 1

    # Test 1b: Conversational prefix removal
    raw2 = 'Here is my analysis:\n{"summary": {"health_score": 50, "risk_level": "MEDIUM", "executive_summary": "issues"}, "findings": []}'
    cleaned2 = sanitize_json(raw2)
    try:
        data2 = json.loads(cleaned2)
        assert validate_json_schema(data2), "Schema validation failed"
        print("  [PASS] 1b: Conversational prefix removal")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] 1b: Conversational prefix removal - {e}")
        failed += 1

    # Test 1c: Trailing text after JSON
    raw3 = '{"summary": {"health_score": 90, "risk_level": "LOW", "executive_summary": "good"}, "findings": []} Hope this helps!'
    cleaned3 = sanitize_json(raw3)
    try:
        data3 = json.loads(cleaned3)
        assert validate_json_schema(data3), "Schema validation failed"
        print("  [PASS] 1c: Trailing text removal")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] 1c: Trailing text removal - {e}")
        failed += 1

    # Test 1d: Invalid schema rejection
    invalid = {"summary": {"health_score": 50}, "findings": []}  # Missing risk_level, executive_summary
    assert not validate_json_schema(invalid), "Should reject invalid schema"
    print("  [PASS] 1d: Invalid schema correctly rejected")
    passed += 1

    # Test 1e: Valid finding schema
    valid = {
        "summary": {"health_score": 70, "risk_level": "MEDIUM", "executive_summary": "test"},
        "findings": [{
            "id": "SEC-001", "category": "SECURITY", "severity": "HIGH",
            "line_numbers": [1], "title": "test", "deep_dive": "test",
            "solution_explanation": "test", "reference": "CWE-89", "fix_code_snippet": "fix"
        }]
    }
    assert validate_json_schema(valid), "Should accept valid schema"
    print("  [PASS] 1e: Valid finding schema accepted")
    passed += 1

    print(f"\n  Parsers: {passed} passed, {failed} failed\n")
    return failed == 0


def test_auto_fixer():
    """Test Python syntax validation (no API calls needed)"""
    print("=" * 60)
    print("TEST 2: Auto Fixer (validate_python_syntax)")
    print("=" * 60)
    passed = 0
    failed = 0

    # Test 2a: Valid Python
    assert validate_python_syntax("x = 1\nprint(x)"), "Should accept valid Python"
    print("  [PASS] 2a: Valid Python accepted")
    passed += 1

    # Test 2b: Invalid Python
    assert not validate_python_syntax("def broken(\n  x ="), "Should reject invalid Python"
    print("  [PASS] 2b: Invalid Python rejected")
    passed += 1

    # Test 2c: Empty string
    assert validate_python_syntax(""), "Should accept empty string"
    print("  [PASS] 2c: Empty string accepted")
    passed += 1

    print(f"\n  Auto Fixer: {passed} passed, {failed} failed\n")
    return failed == 0


def test_git_utils():
    """Test git diff parsing (no API calls needed)"""
    print("=" * 60)
    print("TEST 3: Git Utils (parse_diff_hunks)")
    print("=" * 60)
    passed = 0
    failed = 0

    # Test 3a: Standard diff output
    diff = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -10,5 +10,8 @@
 some code
+new line 1
+new line 2
"""
    files = parse_diff_hunks(diff)
    assert len(files) == 1, f"Expected 1 file, got {len(files)}"
    assert files[0]['path'] == 'src/app.py'
    assert 10 in files[0]['changed_lines']
    print("  [PASS] 3a: Standard diff parsing")
    passed += 1

    # Test 3b: Multiple files
    multi_diff = """diff --git a/file1.py b/file1.py
--- a/file1.py
+++ b/file1.py
@@ -1,3 +1,5 @@
diff --git a/file2.js b/file2.js
--- a/file2.js
+++ b/file2.js
@@ -20,4 +20,6 @@
"""
    multi_files = parse_diff_hunks(multi_diff)
    assert len(multi_files) == 2, f"Expected 2 files, got {len(multi_files)}"
    print("  [PASS] 3b: Multi-file diff parsing")
    passed += 1

    # Test 3c: Empty diff
    empty_files = parse_diff_hunks("")
    assert len(empty_files) == 0, "Empty diff should return no files"
    print("  [PASS] 3c: Empty diff handling")
    passed += 1

    print(f"\n  Git Utils: {passed} passed, {failed} failed\n")
    return failed == 0


# ------------------------------------------------------------------ #
#                       INTEGRATION TESTS                              #
# ------------------------------------------------------------------ #

async def test_core_pipeline():
    """Test the full Finder -> Critic pipeline against a real Balancia file"""
    print("=" * 60)
    print("TEST 4: Core Pipeline (scan_code on real file)")
    print("=" * 60)

    try:
        client = WatsonxClient()
        sentry = QASentry(client)
        print("  Client + Sentry initialized")

        # Find a real TypeScript file in the dataset
        dataset_root = Path(__file__).parent.parent.parent / "dataset_balancia"
        target_file = dataset_root / "src" / "app" / "actions.ts"

        if not target_file.exists():
            # Fallback: find any .ts or .tsx file
            ts_files = list(dataset_root.rglob("*.ts"))
            tsx_files = list(dataset_root.rglob("*.tsx"))
            all_files = ts_files + tsx_files
            if not all_files:
                print("  [SKIP] No TypeScript files found in dataset_balancia")
                return True
            target_file = all_files[0]

        print(f"  Scanning: {target_file.name} ({target_file.stat().st_size} bytes)")
        print("  Running Finder -> Critic pipeline (this takes ~15-30 seconds)...")

        result = await sentry.scan_code(str(target_file), scan_type="all", auto_fix=False)

        if result["success"]:
            summary = result.get("summary", {})
            findings = result.get("findings", [])
            print(f"  [PASS] Scan completed successfully!")
            print(f"         Health Score: {summary.get('health_score', '?')}")
            print(f"         Risk Level:   {summary.get('risk_level', '?')}")
            print(f"         Findings:     {len(findings)}")
            print(f"         Lines:        {result.get('lines_analyzed', '?')}")

            if findings:
                print(f"\n  Top Finding:")
                top = findings[0]
                print(f"    ID:       {top.get('id', '?')}")
                print(f"    Severity: {top.get('severity', '?')}")
                print(f"    Title:    {top.get('title', '?')}")
                preview = top.get('deep_dive', '')[:120]
                print(f"    Details:  {preview}...")

            return True
        else:
            print(f"  [FAIL] Scan failed: {result.get('error', 'Unknown')}")
            return False

    except Exception as e:
        print(f"  [FAIL] Exception: {e}")
        return False


async def test_import_chain():
    """Test that all import paths work after refactor"""
    print("=" * 60)
    print("TEST 5: Import Chain Verification")
    print("=" * 60)
    passed = 0
    failed = 0

    tests = [
        ("lib.utils", "from lib.utils import detect_language, read_file_safe, get_timestamp, format_markdown_header, SUPPORTED_EXTENSIONS"),
        ("lib.utils.constants", "from lib.utils.constants import SUPPORTED_EXTENSIONS"),
        ("lib.utils.file_io", "from lib.utils.file_io import read_file_safe, detect_language"),
        ("lib.utils.formatting", "from lib.utils.formatting import get_timestamp, format_markdown_header"),
        ("lib.qa_sentry", "from lib.qa_sentry import QASentry"),
        ("lib.qa_sentry.core", "from lib.qa_sentry.core import QASentry"),
        ("lib.qa_sentry.parsers", "from lib.qa_sentry.parsers import sanitize_json, validate_json_schema"),
        ("lib.qa_sentry.auto_fixer", "from lib.qa_sentry.auto_fixer import apply_auto_fixes, validate_python_syntax"),
        ("lib.qa_sentry.git_utils", "from lib.qa_sentry.git_utils import parse_diff_hunks"),
        ("lib.autodocs", "from lib.autodocs import AutoDocs"),
        ("lib.autodocs.core", "from lib.autodocs.core import AutoDocs"),
        ("lib.autodocs.prompts", "from lib.autodocs.prompts import get_documentation_prompt"),
    ]

    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name} - {e}")
            failed += 1

    print(f"\n  Import Chain: {passed} passed, {failed} failed\n")
    return failed == 0


# ------------------------------------------------------------------ #
#                       MAIN RUNNER                                    #
# ------------------------------------------------------------------ #

def main():
    print("\n" + "=" * 60)
    print("  QA SENTRY REFACTOR TEST SUITE")
    print("=" * 60 + "\n")

    results = {}

    # Unit tests (no API calls)
    results["parsers"] = test_parsers()
    results["auto_fixer"] = test_auto_fixer()
    results["git_utils"] = test_git_utils()

    # Import chain (no API calls)
    results["imports"] = asyncio.run(test_import_chain())

    # Integration test (calls Watsonx API)
    print("\n  Starting integration test (requires Watsonx API)...\n")
    results["core_pipeline"] = asyncio.run(test_core_pipeline())

    # Final summary
    print("\n" + "=" * 60)
    print("  FINAL RESULTS")
    print("=" * 60)
    all_pass = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        icon = "OK" if passed else "XX"
        print(f"  [{icon}] {name}: {status}")
        if not passed:
            all_pass = False

    if all_pass:
        print(f"\n  ALL TESTS PASSED!")
    else:
        print(f"\n  SOME TESTS FAILED - check output above")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
