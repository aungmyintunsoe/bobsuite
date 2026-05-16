"""
File Manager - Dataset and File Operations Module
Handles reading and managing files from the dataset_balancia test project
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from lib.utils import read_file_safe, format_markdown_header, SUPPORTED_EXTENSIONS


class FileManager:
    """Manages file operations for the dataset_balancia test project"""
    
    def __init__(self, dataset_root: str = "dataset_balancia"):
        """
        Initialize File Manager
        
        Args:
            dataset_root: Root directory of the dataset (relative to project root)
        """
        # Get the project root (parent of mcp_server)
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        
        self.dataset_root = project_root / dataset_root
        # Supported text extensions for reading
        self.supported_text_extensions = set(SUPPORTED_EXTENSIONS.keys()) | {
            '.h', '.hpp', '.scss', '.sass', '.less', '.xml', '.yaml', '.yml', 
            '.toml', '.ini', '.rst', '.tex', '.sh', '.bash', '.zsh', '.fish',
            '.sql', '.graphql', '.proto'
        }
    
    def read_dataset_file(self, relative_path: str) -> str:
        """Read a file from the dataset_balancia directory"""
        file_path = self.dataset_root / relative_path
        
        if not file_path.exists():
            return f"Error: File not found: {relative_path}\nDataset root: {self.dataset_root}"
        
        if not file_path.is_file():
            return f"Error: Path is not a file: {relative_path}"
        
        # Check if file is in supported text formats
        if file_path.suffix.lower() not in self.supported_text_extensions:
            return f"Error: Unsupported file type: {file_path.suffix}"
        
        content, error = read_file_safe(str(file_path))
        if error or content is None:
            return f"Error: {error or 'Failed to read file'}"
            
        return self._format_file_content(relative_path, content, file_path)
    
    def _format_file_content(
        self,
        relative_path: str,
        content: str,
        file_path: Path
    ) -> str:
        """Format file content with metadata"""
        lines = content.count('\n') + 1
        size = file_path.stat().st_size
        
        header = format_markdown_header(f"File: {relative_path}", {
            "full_path": str(file_path),
            "size": f"{size} bytes",
            "lines": lines,
            "type": file_path.suffix
        })
        
        return header + content
    
    def list_dataset_files(
        self,
        pattern: str = "*",
        recursive: bool = True
    ) -> List[str]:
        """List files in the dataset directory"""
        if not self.dataset_root.exists():
            return []
        
        if recursive:
            files = self.dataset_root.rglob(pattern)
        else:
            files = self.dataset_root.glob(pattern)
        
        relative_paths = []
        for file in files:
            if file.is_file():
                relative = file.relative_to(self.dataset_root)
                relative_paths.append(str(relative))
        
        return sorted(relative_paths)
    
    def get_dataset_structure(self) -> Dict[str, Any]:
        """Get the directory structure of the dataset"""
        if not self.dataset_root.exists():
            return {
                "error": f"Dataset directory not found: {self.dataset_root}",
                "exists": False
            }
        
        structure = {
            "root": str(self.dataset_root),
            "exists": True,
            "files": [],
            "directories": [],
            "total_files": 0,
            "total_size": 0
        }
        
        for item in self.dataset_root.rglob("*"):
            relative = item.relative_to(self.dataset_root)
            
            if item.is_file():
                structure["files"].append({
                    "path": str(relative),
                    "size": item.stat().st_size,
                    "extension": item.suffix
                })
                structure["total_files"] += 1
                structure["total_size"] += item.stat().st_size
            elif item.is_dir():
                structure["directories"].append(str(relative))
        
        return structure
    
    def search_in_dataset(
        self,
        search_term: str,
        file_pattern: str = "*.py",
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """Search for a term in dataset files"""
        matches = []
        files = self.list_dataset_files(file_pattern, recursive=True)
        
        for file_path in files:
            full_path = self.dataset_root / file_path
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    search_line = line if case_sensitive else line.lower()
                    search_for = search_term if case_sensitive else search_term.lower()
                    
                    if search_for in search_line:
                        matches.append({
                            "file": file_path,
                            "line": line_num,
                            "content": line.strip(),
                            "match": search_term
                        })
            
            except Exception:
                continue
        
        return matches
    
    def get_file_stats(self, relative_path: str) -> Dict[str, Any]:
        """Get statistics about a file"""
        file_path = self.dataset_root / relative_path
        
        if not file_path.exists():
            return {"error": "File not found", "exists": False}
        
        if not file_path.is_file():
            return {"error": "Path is not a file", "exists": False}
        
        try:
            stat = file_path.stat()
            content, error = read_file_safe(str(file_path))
            
            if error or content is None:
                return {"error": error or "Failed to read file", "exists": True}
                
            lines = content.count('\n') + 1
            chars = len(content)
            words = len(content.split())
            
            return {
                "exists": True,
                "path": relative_path,
                "size_bytes": stat.st_size,
                "lines": lines,
                "characters": chars,
                "words": words,
                "extension": file_path.suffix,
                "modified": stat.st_mtime,
                "created": stat.st_ctime
            }
        
        except Exception as e:
            return {"error": str(e), "exists": True}
    
    def create_file_index(self) -> Dict[str, List[str]]:
        """Create an index of files by extension"""
        index = {}
        files = self.list_dataset_files("*", recursive=True)
        
        for file_path in files:
            ext = Path(file_path).suffix or "no_extension"
            if ext not in index:
                index[ext] = []
            index[ext].append(file_path)
        
        return index

# Made with Bob
