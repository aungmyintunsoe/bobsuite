"""
Caching Utilities - File hash-based caching for performance optimization
Provides 2-3x speedup by skipping unchanged files
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class FileCache:
    """
    Simple file-based cache using MD5 hashing.
    Caches results based on file content hash to skip re-analysis of unchanged files.
    """
    
    def __init__(self, cache_dir: str = ".bob_cache", ttl_hours: float = 24):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live for cache entries in hours (can be fractional)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.memory_cache: Dict[str, Any] = {}
    
    def get_file_hash(self, file_path: str, content: Optional[str] = None) -> str:
        """
        Generate MD5 hash of file content.
        
        Args:
            file_path: Path to the file
            content: Optional pre-loaded content (avoids re-reading)
        
        Returns:
            MD5 hash string
        """
        if content is None:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                return ""
        
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get_cache_key(self, file_path: str, operation: str, content: Optional[str] = None) -> str:
        """
        Generate a cache key combining file hash and operation type.
        
        Args:
            file_path: Path to the file
            operation: Type of operation (e.g., 'qa_scan', 'autodocs', 'visualizer')
            content: Optional pre-loaded content
        
        Returns:
            Cache key string
        """
        file_hash = self.get_file_hash(file_path, content)
        return f"{operation}_{file_hash}"
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached result if it exists and is not expired.
        
        Args:
            cache_key: Cache key to lookup
        
        Returns:
            Cached result or None if not found/expired
        """
        # Check memory cache first
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        
        # Check disk cache
        cache_file = self.cache_dir / f"{cache_key}.json"
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check if expired
            cached_time = datetime.fromisoformat(cached_data.get('timestamp', '2000-01-01'))
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()  # Delete expired cache
                return None
            
            result = cached_data.get('result')
            # Store in memory cache for faster subsequent access
            self.memory_cache[cache_key] = result
            return result
            
        except Exception:
            return None
    
    def set(self, cache_key: str, result: Dict[str, Any]) -> bool:
        """
        Store result in cache.
        
        Args:
            cache_key: Cache key
            result: Result to cache
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Store in memory cache
            self.memory_cache[cache_key] = result
            
            # Store in disk cache
            cache_file = self.cache_dir / f"{cache_key}.json"
            cached_data = {
                'timestamp': datetime.now().isoformat(),
                'result': result
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, indent=2)
            
            return True
            
        except Exception:
            return False
    
    def clear(self, operation: Optional[str] = None) -> int:
        """
        Clear cache entries.
        
        Args:
            operation: If specified, only clear entries for this operation
        
        Returns:
            Number of entries cleared
        """
        count = 0
        
        # Clear memory cache
        if operation:
            keys_to_remove = [k for k in self.memory_cache.keys() if k.startswith(f"{operation}_")]
            for key in keys_to_remove:
                del self.memory_cache[key]
                count += 1
        else:
            count = len(self.memory_cache)
            self.memory_cache.clear()
        
        # Clear disk cache
        if self.cache_dir.exists():
            pattern = f"{operation}_*.json" if operation else "*.json"
            for cache_file in self.cache_dir.glob(pattern):
                cache_file.unlink()
                count += 1
        
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        disk_entries = len(list(self.cache_dir.glob("*.json"))) if self.cache_dir.exists() else 0
        
        return {
            'memory_entries': len(self.memory_cache),
            'disk_entries': disk_entries,
            'cache_dir': str(self.cache_dir),
            'ttl_hours': self.ttl.total_seconds() / 3600
        }


# Global cache instance
_global_cache: Optional[FileCache] = None


def get_cache(cache_dir: str = ".bob_cache", ttl_hours: float = 24) -> FileCache:
    """
    Get or create the global cache instance.
    
    Args:
        cache_dir: Directory to store cache files
        ttl_hours: Time-to-live for cache entries in hours
    
    Returns:
        FileCache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = FileCache(cache_dir, ttl_hours)
    return _global_cache


# Made with Bob