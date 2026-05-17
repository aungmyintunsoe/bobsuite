"""
QA Sentry - Core Orchestrator
Multi-Agent AI Scanner with Debate Pattern (Finder vs. Critic)

This is the main entry point. It orchestrates:
- File reading and language detection
- Context chunking for large files (>1000 lines, optimized from 500)
- Two-pass AI analysis (Finder → Critic)
- Auto-fix delegation
- Git diff delegation
- Report generation

OPTIMIZATIONS:
- Increased chunk size from 500 to 1000 lines (50% fewer API calls)
- File hash-based caching (skip unchanged files)
- Concurrent batch scanning with asyncio.gather()
- Extracted prompts for easier maintenance
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from lib.utils import detect_language, get_timestamp, read_file_safe, format_markdown_header
from lib.utils.cache import get_cache
from lib.qa_sentry.parsers import sanitize_json, validate_json_schema, FALLBACK_RESULT
from lib.qa_sentry.auto_fixer import apply_auto_fixes
from lib.qa_sentry.git_utils import scan_git_diff as _scan_git_diff
from lib.qa_sentry.prompts import (
    build_finder_prompt,
    build_critic_prompt,
    build_network_performance_test_prompt,
    build_unit_test_generation_prompt
)


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
    #                       AGENT PASSES                                  #
    # ------------------------------------------------------------------ #

    async def _finder_pass(
        self,
        code: str,
        language: str,
        file_path: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pass 1: The Finder - Aggressive issue detection.

        Returns raw JSON with all potential issues.
        """
        prompt = build_finder_prompt(
            code=code,
            language=language,
            file_path=file_path,
            system_context=self.system_prompt,
            additional_context=additional_context
        )

        try:
            response = await self.watsonx.generate_text(
                prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            clean_json = sanitize_json(response)
            data = json.loads(clean_json)

            if not validate_json_schema(data):
                raise ValueError("Response does not match expected schema")

            return data
        except json.JSONDecodeError as e:
            return {
                "summary": {
                    "health_score": 50,
                    "risk_level": "MEDIUM",
                    "executive_summary": f"JSON parsing error in Finder pass: {str(e)}"
                },
                "findings": []
            }
        except Exception as e:
            return {
                "summary": {
                    "health_score": 50,
                    "risk_level": "MEDIUM",
                    "executive_summary": f"Error in Finder pass: {str(e)}"
                },
                "findings": []
            }

    async def _critic_pass(
        self,
        code: str,
        finder_results: Dict[str, Any],
        language: str,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Pass 2: The Critic - Verification and pruning of false positives.

        Returns hardened, verified JSON.
        """
        prompt = build_critic_prompt(
            code=code,
            finder_results=finder_results,
            language=language,
            file_path=file_path
        )

        try:
            response = await self.watsonx.generate_text(
                prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            clean_json = sanitize_json(response)
            data = json.loads(clean_json)

            if not validate_json_schema(data):
                # If Critic fails validation, return Finder results
                return finder_results

            return data
        except Exception:
            # If Critic fails, return Finder results
            return finder_results

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
                result = await self._chunk_and_analyze(code, file_path, language, additional_context)
            else:
                # Standard two-pass analysis
                finder_results = await self._finder_pass(code, language, file_path, additional_context)
                final_results = await self._critic_pass(code, finder_results, language, file_path)

                result = {
                    "success": True,
                    "file_path": file_path,
                    "language": language,
                    "scan_type": scan_type,
                    "timestamp": get_timestamp(),
                    "summary": final_results.get("summary", {}),
                    "findings": final_results.get("findings", []),
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
            return {
                "success": False,
                "error": f"Unexpected error during scan: {str(e)}",
                "error_type": type(e).__name__,
                "file_path": file_path
            }

    # ------------------------------------------------------------------ #
    #                       CHUNKING                                      #
    # ------------------------------------------------------------------ #

    async def _chunk_and_analyze(
        self,
        code: str,
        file_path: str,
        language: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Split large files into chunks and analyze concurrently."""
        lines = code.split('\n')
        chunks = []

        for i in range(0, len(lines), self.chunk_size):
            chunk_lines = lines[i:i + self.chunk_size]
            chunk_code = '\n'.join(chunk_lines)
            chunks.append({
                'code': chunk_code,
                'start_line': i + 1,
                'end_line': min(i + self.chunk_size, len(lines))
            })

        # Analyze chunks concurrently
        tasks = [
            self._analyze_chunk(chunk, file_path, language, additional_context)
            for chunk in chunks
        ]

        chunk_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Merge results
        all_findings = []
        total_health_score = 0
        valid_chunks = 0

        for result in chunk_results:
            if isinstance(result, dict) and 'findings' in result:
                all_findings.extend(result['findings'])
                total_health_score += result.get('summary', {}).get('health_score', 50)
                valid_chunks += 1

        avg_health_score = total_health_score // valid_chunks if valid_chunks > 0 else 50

        if avg_health_score < 30:
            risk_level = "CRITICAL"
        elif avg_health_score < 50:
            risk_level = "HIGH"
        elif avg_health_score < 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "success": True,
            "file_path": file_path,
            "language": language,
            "timestamp": get_timestamp(),
            "summary": {
                "health_score": avg_health_score,
                "risk_level": risk_level,
                "executive_summary": f"Large file analyzed in {len(chunks)} chunks with {len(all_findings)} total findings"
            },
            "findings": all_findings,
            "lines_analyzed": len(lines),
            "chunks_processed": len(chunks)
        }

    async def _analyze_chunk(
        self,
        chunk: Dict[str, Any],
        file_path: str,
        language: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze a single chunk of code."""
        try:
            finder_results = await self._finder_pass(
                chunk['code'],
                language,
                f"{file_path} (lines {chunk['start_line']}-{chunk['end_line']})",
                additional_context
            )

            # Adjust line numbers to reflect actual file position
            for finding in finder_results.get('findings', []):
                finding['line_numbers'] = [
                    ln + chunk['start_line'] - 1
                    for ln in finding.get('line_numbers', [])
                ]

            return finder_results
        except Exception as e:
            return {
                "summary": {
                    "health_score": 50,
                    "risk_level": "MEDIUM",
                    "executive_summary": f"Error analyzing chunk: {str(e)}"
                },
                "findings": []
            }

    # ------------------------------------------------------------------ #
    #                       CROSS-FILE CONTEXT                            #
    # ------------------------------------------------------------------ #

    async def _build_cross_file_context(self, file_paths: List[str]) -> str:
        """Extract interfaces/signatures from related files for context."""
        context_parts = []

        for path in file_paths:
            code, error = read_file_safe(path)
            if code:
                lines = code.split('\n')[:50]
                signatures = '\n'.join(lines)
                context_parts.append(f"# {path}\n{signatures}\n")

        return "\n".join(context_parts)

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
            additional_context = await self._build_cross_file_context(file_paths)

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
        staged: bool = True
    ) -> List[Dict[str, Any]]:
        """Scan only changed lines from git diff (delegates to git_utils)."""
        return await _scan_git_diff(self, repo_path, staged)

    # ------------------------------------------------------------------ #
    #                       TESTING FEATURES                              #
    # ------------------------------------------------------------------ #

    async def generate_network_performance_tests(
        self,
        file_path: str,
        testing_library: Optional[str] = None,
        test_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive network performance tests for API endpoints and network calls.
        
        Args:
            file_path: Path to the code file containing network/API code
            testing_library: Optional specific testing library (e.g., 'jest', 'postman', 'pytest')
            test_requirements: Optional specific requirements for the tests
        
        Returns:
            Dictionary containing test files, setup commands, and execution instructions
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

            # Detect language
            language = detect_language(file_path)
            if not language or language == "Unknown":
                language = "text"

            # Build the prompt
            prompt = build_network_performance_test_prompt(
                code=code,
                language=language,
                file_path=file_path,
                testing_library=testing_library,
                test_requirements=test_requirements
            )

            # Generate tests using watsonx
            response = await self.watsonx.generate_text(
                prompt,
                temperature=0.2,  # Slightly higher for creative test generation
                max_tokens=6000   # More tokens for comprehensive test suites
            )

            # Parse the JSON response
            clean_json = sanitize_json(response)
            test_data = json.loads(clean_json)

            # Add metadata
            result = {
                "success": True,
                "file_path": file_path,
                "language": language,
                "timestamp": get_timestamp(),
                "test_type": "network_performance",
                "test_framework": test_data.get("test_framework"),
                "framework_justification": test_data.get("framework_justification"),
                "dependencies": test_data.get("dependencies", []),
                "setup_commands": test_data.get("setup_commands", []),
                "test_files": test_data.get("test_files", []),
                "execution_command": test_data.get("execution_command"),
                "configuration_files": test_data.get("configuration_files", []),
                "performance_thresholds": test_data.get("performance_thresholds", {}),
                "test_scenarios": test_data.get("test_scenarios", []),
                "notes": test_data.get("notes", "")
            }

            return result

        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON parsing error: {str(e)}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": type(e).__name__,
                "file_path": file_path
            }

    async def generate_unit_tests(
        self,
        file_path: str,
        testing_library: Optional[str] = None,
        test_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive unit tests following Steve Sanderson principles.
        
        Args:
            file_path: Path to the code file to generate unit tests for
            testing_library: Optional specific testing library (e.g., 'jest', 'pytest', 'junit')
            test_requirements: Optional specific requirements for the tests
        
        Returns:
            Dictionary containing test files, setup commands, and execution instructions
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

            # Detect language
            language = detect_language(file_path)
            if not language or language == "Unknown":
                language = "text"

            # Build the prompt
            prompt = build_unit_test_generation_prompt(
                code=code,
                language=language,
                file_path=file_path,
                testing_library=testing_library,
                test_requirements=test_requirements
            )

            # Generate tests using watsonx
            response = await self.watsonx.generate_text(
                prompt,
                temperature=0.2,  # Slightly higher for creative test generation
                max_tokens=6000   # More tokens for comprehensive test suites
            )

            # Parse the JSON response
            clean_json = sanitize_json(response)
            test_data = json.loads(clean_json)

            # Add metadata
            result = {
                "success": True,
                "file_path": file_path,
                "language": language,
                "timestamp": get_timestamp(),
                "test_type": "unit_tests",
                "test_framework": test_data.get("test_framework"),
                "framework_justification": test_data.get("framework_justification"),
                "dependencies": test_data.get("dependencies", []),
                "setup_commands": test_data.get("setup_commands", []),
                "test_files": test_data.get("test_files", []),
                "execution_command": test_data.get("execution_command"),
                "configuration_files": test_data.get("configuration_files", []),
                "mock_strategy": test_data.get("mock_strategy", {}),
                "test_coverage": test_data.get("test_coverage", {}),
                "design_principles_applied": test_data.get("design_principles_applied", []),
                "notes": test_data.get("notes", "")
            }

            return result

        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON parsing error: {str(e)}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": type(e).__name__,
                "file_path": file_path
            }

    # ------------------------------------------------------------------ #
    #                       REPORTING                                     #
    # ------------------------------------------------------------------ #

    def generate_report(
        self,
        scan_results: List[Dict[str, Any]],
        output_path: Optional[str] = None
    ) -> str:
        """Generate a markdown report from scan results."""
        report_lines = [
            format_markdown_header("Code Quality Analysis Report", {
                "generated": get_timestamp(),
                "total_files_scanned": len(scan_results)
            })
        ]

        for result in scan_results:
            if not result.get("success"):
                report_lines.append(f"\n## {result.get('file_path', 'Unknown')}")
                report_lines.append(f"\n**Error:** {result.get('error', 'Unknown error')}\n")
                continue

            summary = result.get("summary", {})
            report_lines.append(f"\n## {result['file_path']}")
            report_lines.append(f"\n**Language:** {result.get('language', 'Unknown')}")
            report_lines.append(f"\n**Health Score:** {summary.get('health_score', 'N/A')}")
            report_lines.append(f"\n**Risk Level:** {summary.get('risk_level', 'N/A')}")
            report_lines.append(f"\n**Findings:** {len(result.get('findings', []))}")

            for finding in result.get('findings', []):
                report_lines.append(f"\n\n### [{finding.get('severity', '?')}] {finding.get('title', 'Untitled')}")
                report_lines.append(f"\n**Lines:** {finding.get('line_numbers', [])}")
                report_lines.append(f" | **ID:** {finding.get('id', '?')} | **Category:** {finding.get('category', '?')}")
                
                report_lines.append(f"\n\n#### The Problem")
                report_lines.append(f"\n> {finding.get('deep_dive', 'N/A')}")
                
                report_lines.append(f"\n\n#### The Solution")
                if finding.get('solution_explanation'):
                    report_lines.append(f"\n{finding.get('solution_explanation')}")
                
                if finding.get('fix_code_snippet'):
                    report_lines.append(f"\n\n```python\n{finding['fix_code_snippet']}\n```")
                
                report_lines.append(f"\n\n**Reference:** {finding.get('reference', 'N/A')}")

            report_lines.append("\n\n---\n")

        report = "\n".join(report_lines)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)

        return report


# Made with Bob
