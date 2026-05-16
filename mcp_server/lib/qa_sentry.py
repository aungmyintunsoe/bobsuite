"""
QA Sentry - Code Quality Analysis Module
Scans code for bugs, vulnerabilities, and quality issues using watsonx.ai
"""

from typing import Dict, Any, List, Optional
from lib.utils import detect_language, get_timestamp, read_file_safe, format_markdown_header


class QASentry:
    """Code quality analysis and bug detection"""
    
    def __init__(self, watsonx_client):
        """
        Initialize QA Sentry
        
        Args:
            watsonx_client: WatsonxClient instance for AI analysis
        """
        self.watsonx = watsonx_client
    
    async def scan_code(
        self,
        file_path: str,
        scan_type: str = "all"
    ) -> Dict[str, Any]:
        """
        Scan code file for issues
        
        Args:
            file_path: Path to the code file
            scan_type: Type of scan (bugs, vulnerabilities, quality, all)
            
        Returns:
            Dictionary containing scan results
        """
        # Read the file
        code, error = read_file_safe(file_path)
        if error:
            return {
                "error": error,
                "success": False
            }
        
        # Detect language
        language = detect_language(file_path)
        
        # Perform analysis
        analysis = await self.watsonx.analyze_code(
            code=code,
            analysis_type=scan_type,
            language=language
        )
        
        # Parse and structure results
        results = self._structure_results(analysis, file_path, scan_type)
        
        return results
    
    def _structure_results(
        self,
        analysis: Dict[str, Any],
        file_path: str,
        scan_type: str
    ) -> Dict[str, Any]:
        """Structure the analysis results into a standardized format"""
        return {
            "success": True,
            "file_path": file_path,
            "language": analysis.get("language", "Unknown"),
            "scan_type": scan_type,
            "timestamp": get_timestamp(),
            "analysis": analysis.get("results", ""),
            "summary": self._generate_summary(analysis.get("results", ""))
        }
    
    def _generate_summary(self, analysis_text: str) -> Dict[str, Any]:
        """Generate a summary from the analysis text"""
        lines = analysis_text.lower().split('\n')
        
        summary = {
            "total_issues": 0,
            "critical": 0,
            "warnings": 0,
            "suggestions": 0,
            "has_vulnerabilities": False,
            "has_bugs": False
        }
        
        for line in lines:
            if any(word in line for word in ['critical', 'severe', 'high risk']):
                summary["critical"] += 1
                summary["total_issues"] += 1
            elif any(word in line for word in ['warning', 'moderate', 'medium']):
                summary["warnings"] += 1
                summary["total_issues"] += 1
            elif any(word in line for word in ['suggestion', 'improvement', 'consider']):
                summary["suggestions"] += 1
            
            if 'vulnerability' in line or 'security' in line:
                summary["has_vulnerabilities"] = True
            if 'bug' in line or 'error' in line:
                summary["has_bugs"] = True
        
        return summary
    
    async def batch_scan(
        self,
        file_paths: List[str],
        scan_type: str = "all"
    ) -> List[Dict[str, Any]]:
        """Scan multiple files"""
        results = []
        for file_path in file_paths:
            result = await self.scan_code(file_path, scan_type)
            results.append(result)
        
        return results
    
    def generate_report(
        self,
        scan_results: List[Dict[str, Any]],
        output_path: Optional[str] = None
    ) -> str:
        """Generate a markdown report from scan results"""
        report_lines = [
            format_markdown_header("Code Quality Analysis Report", {
                "generated": get_timestamp(),
                "total_files_scanned": len(scan_results)
            })
        ]
        
        for result in scan_results:
            if not result.get("success"):
                report_lines.append(f"\n## ❌ {result.get('file_path', 'Unknown')}")
                report_lines.append(f"\n**Error:** {result.get('error', 'Unknown error')}\n")
                continue
            
            summary = result.get("summary", {})
            report_lines.append(f"\n## 📄 {result['file_path']}")
            report_lines.append(f"\n**Language:** {result.get('language', 'Unknown')}")
            report_lines.append(f"\n**Scan Type:** {result.get('scan_type', 'all')}")
            report_lines.append(f"\n\n### Summary")
            report_lines.append(f"\n- Total Issues: {summary.get('total_issues', 0)}")
            report_lines.append(f"\n- Critical: {summary.get('critical', 0)}")
            report_lines.append(f"\n- Warnings: {summary.get('warnings', 0)}")
            report_lines.append(f"\n- Suggestions: {summary.get('suggestions', 0)}")
            
            if summary.get('has_vulnerabilities'):
                report_lines.append("\n- ⚠️ Security vulnerabilities detected")
            if summary.get('has_bugs'):
                report_lines.append("\n- 🐛 Potential bugs detected")
            
            report_lines.append(f"\n\n### Detailed Analysis\n\n{result.get('analysis', 'No analysis available')}")
            report_lines.append("\n\n---\n")
        
        report = "\n".join(report_lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report

# Made with Bob
