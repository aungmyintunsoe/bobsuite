"""
QA Sentry - Core Orchestrator
Multi-Agent AI Scanner with Debate Pattern (Finder vs. Critic)

This is the main entry point. It orchestrates:
- File reading and language detection
- Context chunking for large files (>1000 lines, optimized from 500)
- Two-pass AI analysis (Finder → Critic)
- Auto-fix delegation
- Git diff delegation
- Dynamic test generation (unit, network, integration, e2e, etc.)
- Report generation

OPTIMIZATIONS:
- Increased chunk size from 500 to 1000 lines (50% fewer API calls)
- File hash-based caching (skip unchanged files)
- Concurrent batch scanning with asyncio.gather()
- Extracted prompts for easier maintenance

ARCHITECTURE (refactored):
- agents.py      → Finder/Critic debate passes
- chunking.py    → Large file splitting + concurrent analysis
- test_generator → Dynamic test generation (loads test_persona.txt)
- reporting.py   → Markdown report generation
- prompts.py     → Centralized prompt templates
- parsers.py     → JSON sanitization + schema validation
- auto_fixer.py  → Code fix application
- git_utils.py   → Git diff scanning
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional

from lib.utils import detect_language, get_timestamp, read_file_safe
from lib.utils.cache import get_cache
from lib.qa_sentry.agents import finder_pass, critic_pass
from lib.qa_sentry.chunking import chunk_and_analyze, build_cross_file_context
from lib.qa_sentry.auto_fixer import apply_auto_fixes
from lib.qa_sentry.git_utils import scan_git_diff as _scan_git_diff
from lib.qa_sentry.test_generator import generate_tests
from lib.qa_sentry.reporting import generate_report as _generate_report


class QASentry:
    """Production-grade code quality analysis with multi-agent verification"""

    def __init__(self, watsonx_client, enable_cache: bool = True):
        """
        Initialize QA Sentry with enhanced capabilities.

        Args:
            watsonx_client: WatsonxClient instance for AI analysis
            enable_cache: Enable file hash-based caching for performance
        """
        self.watsonx = watsonx_client
        self.system_prompt = self._load_system_context()
        self.temperature = 0.1  # Strict technical mode
        self.max_tokens = 4000
        self.chunk_size = 1000  # Lines per chunk (optimized from 500 to 1000)
        self.enable_cache = enable_cache
        self.cache = get_cache() if enable_cache else None

    def _load_system_context(self) -> str:
        """Load the comprehensive system prompt with few-shot examples"""
        # Try loading from the reviewer.txt file first
        try:
            prompt_path = Path(__file__).parent / "reviewer.txt"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            pass

        # Fallback: try system_context.md in prompts/
        try:
            prompt_path = Path(__file__).parent.parent.parent / "prompts" / "system_context.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            # Fallback to basic prompt
            return """You are an elite code auditor. Analyze code for bugs, vulnerabilities, and quality issues.
Return ONLY valid JSON with this schema:
{
  "summary": {"health_score": 0-100, "risk_level": "CRITICAL|HIGH|MEDIUM|LOW", "executive_summary": "string"},
  "findings": [{"id": "string", "category": "string", "severity": "string", "line_numbers": [], "title": "string", "deep_dive": "string", "solution_explanation": "string", "reference": "string", "fix_code_snippet": "string"}]
}"""

    # ------------------------------------------------------------------ #
    #                       MAIN PIPELINE                                 #
    # ------------------------------------------------------------------ #

    async def scan_code(
        self,
        file_path: str,
        scan_type: str = "all",
        auto_fix: bool = False,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Production-grade code scanning with multi-agent debate pattern and caching.

        Args:
            file_path: Path to the code file
            scan_type: Type of scan (bugs, vulnerabilities, quality, all)
            auto_fix: If True, automatically apply suggested fixes
            additional_context: Optional cross-file context

        Returns:
            Dictionary containing comprehensive scan results
        """
        try:
            # Read the file
            code, error = read_file_safe(file_path)
            if error or code is None:
                return {
                    "success": False,
                    "error": error or "Failed to read file",
                    "file_path": file_path
                }

            # Check cache first (skip if auto_fix is requested)
            cache_key = None
            if self.enable_cache and self.cache and not auto_fix:
                cache_key = self.cache.get_cache_key(file_path, f"qa_sentry_{scan_type}", code)
                cached_result = self.cache.get(cache_key)
                if cached_result:
                    cached_result['from_cache'] = True
                    return cached_result

            # Detect language
            language = detect_language(file_path)
            if not language or language == "Unknown":
                language = "text"

            # Check if chunking is needed
            lines = code.split('\n')
            if len(lines) > self.chunk_size:
                result = await chunk_and_analyze(
                    self.watsonx, code, file_path, language,
                    self.system_prompt, self.chunk_size,
                    self.temperature, self.max_tokens,
                    additional_context
                )
            else:
                # Standard two-pass analysis
                finder_results = await finder_pass(
                    self.watsonx, code, language, file_path,
                    self.system_prompt, self.temperature, self.max_tokens,
                    additional_context
                )
                
                # Ensure finder_results is a dict
                if not isinstance(finder_results, dict):
                    finder_results = {
                        "summary": {"health_score": 50, "risk_level": "MEDIUM", "executive_summary": "Invalid finder results"},
                        "findings": []
                    }
                
                final_results = await critic_pass(
                    self.watsonx, code, finder_results, language, file_path,
                    self.temperature, self.max_tokens
                )
                
                # Ensure final_results is a dict
                if not isinstance(final_results, dict):
                    final_results = {
                        "summary": {"health_score": 50, "risk_level": "MEDIUM", "executive_summary": "Invalid critic results"},
                        "findings": []
                    }

                # Ensure findings is a list, not a set
                findings = final_results.get("findings", [])
                if isinstance(findings, set):
                    findings = list(findings)
                elif not isinstance(findings, list):
                    findings = []
                
                result = {
                    "success": True,
                    "file_path": file_path,
                    "language": language,
                    "scan_type": scan_type,
                    "timestamp": get_timestamp(),
                    "summary": final_results.get("summary", {}),
                    "findings": findings,
                    "lines_analyzed": len(lines)
                }

            # Cache the result (before auto-fix)
            if self.enable_cache and self.cache and cache_key and not auto_fix:
                self.cache.set(cache_key, result)

            # Apply auto-fix if requested
            if auto_fix and result.get("success") and result.get("findings"):
                fix_result = await apply_auto_fixes(file_path, result["findings"])
                result["auto_fix_applied"] = fix_result

            return result

        except Exception as e:
            import traceback
            return {
                "success": False,
                "error": f"Unexpected error during scan: {str(e)}",
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
                "file_path": file_path
            }

    # ------------------------------------------------------------------ #
    #                       BATCH & GIT                                   #
    # ------------------------------------------------------------------ #

    async def batch_scan(
        self,
        file_paths: List[str],
        scan_type: str = "all",
        auto_fix: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Scan multiple files with concurrent execution and optional cross-file context.
        
        OPTIMIZATION: Uses asyncio.gather() for concurrent scanning (2-5x faster).
        """
        additional_context = None
        if len(file_paths) <= 5:
            additional_context = await build_cross_file_context(file_paths)

        # Scan all files concurrently
        results = await asyncio.gather(*[
            self.scan_code(
                file_path,
                scan_type,
                auto_fix=auto_fix,
                additional_context=additional_context
            )
            for file_path in file_paths
        ], return_exceptions=True)
        
        # Convert exceptions to error results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": f"Exception during scan: {str(result)}",
                    "error_type": type(result).__name__,
                    "file_path": file_paths[i]
                })
            else:
                processed_results.append(result)
        
        return processed_results

    async def scan_git_diff(
        self,
        repo_path: str,
        staged: bool = True,
        max_files: int = 10,
        max_file_size_kb: int = 500
    ) -> List[Dict[str, Any]]:
        """Scan only changed lines from git diff with configurable limits (delegates to git_utils)."""
        return await _scan_git_diff(self, repo_path, staged, max_files, max_file_size_kb)

    # ------------------------------------------------------------------ #
    #                       TEST GENERATION                               #
    # ------------------------------------------------------------------ #

    async def generate_network_performance_tests(
        self,
        file_path: str,
        testing_library: Optional[str] = None,
        test_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive network performance tests.
        Delegates to the unified test generator with test_type='network'.
        """
        return await generate_tests(
            self.watsonx,
            file_path,
            test_type="network",
            testing_library=testing_library,
            test_requirements=test_requirements
        )

    async def generate_unit_tests(
        self,
        file_path: str,
        testing_library: Optional[str] = None,
        test_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive unit tests following Steve Sanderson principles.
        Delegates to the unified test generator with test_type='unit'.
        """
        return await generate_tests(
            self.watsonx,
            file_path,
            test_type="unit",
            testing_library=testing_library,
            test_requirements=test_requirements
        )

    # ------------------------------------------------------------------ #
    #                       REPORTING                                     #
    # ------------------------------------------------------------------ #

    def generate_report(
        self,
        scan_results: List[Dict[str, Any]],
        output_path: Optional[str] = None
    ) -> str:
        """Generate a markdown report from scan results."""
        return _generate_report(scan_results, output_path)


# Made with Bob
