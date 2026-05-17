"""
Comprehensive tests for the file hash-based caching system
Tests cache hits, misses, TTL, invalidation, and edge cases
"""

import pytest
import asyncio
import time
from pathlib import Path
import tempfile
import shutil
from lib.utils.cache import FileCache, get_cache


class TestFileCache:
    """Test suite for FileCache functionality"""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def cache(self, temp_cache_dir):
        """Create a FileCache instance for testing"""
        return FileCache(cache_dir=temp_cache_dir, ttl_hours=1)
    
    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("def hello():\n    return 'world'\n")
            temp_path = f.name
        yield temp_path
        Path(temp_path).unlink(missing_ok=True)
    
    def test_cache_initialization(self, temp_cache_dir):
        """Test cache initialization creates directory"""
        cache = FileCache(cache_dir=temp_cache_dir)
        assert Path(temp_cache_dir).exists()
        assert cache.ttl.total_seconds() == 24 * 3600  # Default 24 hours
    
    def test_get_file_hash(self, cache, temp_file):
        """Test file hash generation"""
        hash1 = cache.get_file_hash(temp_file)
        assert hash1
        assert len(hash1) == 32  # MD5 hash length
        
        # Same file should produce same hash
        hash2 = cache.get_file_hash(temp_file)
        assert hash1 == hash2
    
    def test_get_file_hash_with_content(self, cache):
        """Test hash generation with pre-loaded content"""
        content = "test content"
        hash1 = cache.get_file_hash("dummy.py", content)
        hash2 = cache.get_file_hash("dummy.py", content)
        assert hash1 == hash2
    
    def test_get_cache_key(self, cache, temp_file):
        """Test cache key generation"""
        key1 = cache.get_cache_key(temp_file, "autodocs")
        assert key1.startswith("autodocs_")
        
        key2 = cache.get_cache_key(temp_file, "qa_sentry")
        assert key2.startswith("qa_sentry_")
        
        # Different operations should have different keys
        assert key1 != key2
    
    def test_cache_set_and_get(self, cache, temp_file):
        """Test basic cache set and get operations"""
        cache_key = cache.get_cache_key(temp_file, "test_op")
        test_data = {"result": "success", "value": 42}
        
        # Set cache
        assert cache.set(cache_key, test_data)
        
        # Get cache
        cached_data = cache.get(cache_key)
        assert cached_data == test_data
    
    def test_cache_miss(self, cache):
        """Test cache miss returns None"""
        result = cache.get("nonexistent_key")
        assert result is None
    
    def test_cache_invalidation_on_content_change(self, cache, temp_file):
        """Test cache invalidates when file content changes"""
        # Cache original content
        with open(temp_file, 'r') as f:
            original_content = f.read()
        
        key1 = cache.get_cache_key(temp_file, "test_op", original_content)
        cache.set(key1, {"version": 1})
        
        # Modify file
        with open(temp_file, 'w') as f:
            f.write("def hello():\n    return 'modified'\n")
        
        with open(temp_file, 'r') as f:
            new_content = f.read()
        
        # New content should generate different key
        key2 = cache.get_cache_key(temp_file, "test_op", new_content)
        assert key1 != key2
        
        # Old key should still have cached data
        assert cache.get(key1) == {"version": 1}
        
        # New key should be a cache miss
        assert cache.get(key2) is None
    
    def test_memory_cache(self, cache, temp_file):
        """Test memory cache for fast repeated access"""
        cache_key = cache.get_cache_key(temp_file, "test_op")
        test_data = {"fast": "access"}
        
        cache.set(cache_key, test_data)
        
        # First get (from disk)
        result1 = cache.get(cache_key)
        assert result1 == test_data
        
        # Second get (from memory)
        result2 = cache.get(cache_key)
        assert result2 == test_data
        
        # Should be in memory cache
        assert cache_key in cache.memory_cache
    
    def test_cache_ttl_expiration(self, temp_cache_dir):
        """Test cache entries expire after TTL"""
        # Create cache with 1 second TTL
        cache = FileCache(cache_dir=temp_cache_dir, ttl_hours=1/3600)  # 1 second
        
        cache_key = "test_key"
        cache.set(cache_key, {"data": "expires"})
        
        # Should be available immediately
        assert cache.get(cache_key) is not None
        
        # Wait for expiration
        time.sleep(2)
        
        # Should be expired
        assert cache.get(cache_key) is None
    
    def test_cache_clear_all(self, cache, temp_file):
        """Test clearing all cache entries"""
        # Add multiple entries
        for i in range(5):
            key = cache.get_cache_key(temp_file, f"op_{i}")
            cache.set(key, {"index": i})
        
        # Clear all
        count = cache.clear()
        assert count >= 5
        
        # All should be cleared
        for i in range(5):
            key = cache.get_cache_key(temp_file, f"op_{i}")
            assert cache.get(key) is None
    
    def test_cache_clear_by_operation(self, cache, temp_file):
        """Test clearing cache entries for specific operation"""
        # Add entries for different operations
        key1 = cache.get_cache_key(temp_file, "autodocs")
        key2 = cache.get_cache_key(temp_file, "qa_sentry")
        
        cache.set(key1, {"op": "autodocs"})
        cache.set(key2, {"op": "qa_sentry"})
        
        # Clear only autodocs
        cache.clear(operation="autodocs")
        
        # autodocs should be cleared
        assert cache.get(key1) is None
        
        # qa_sentry should still exist
        assert cache.get(key2) == {"op": "qa_sentry"}
    
    def test_cache_stats(self, cache, temp_file):
        """Test cache statistics"""
        # Add some entries
        for i in range(3):
            key = cache.get_cache_key(temp_file, f"op_{i}")
            cache.set(key, {"index": i})
        
        stats = cache.get_stats()
        assert stats['memory_entries'] == 3
        assert stats['disk_entries'] >= 3
        assert 'cache_dir' in stats
        assert stats['ttl_hours'] == 1
    
    def test_concurrent_cache_access(self, cache, temp_file):
        """Test concurrent cache access doesn't cause issues"""
        async def set_and_get(index):
            key = cache.get_cache_key(temp_file, f"concurrent_{index}")
            cache.set(key, {"index": index})
            result = cache.get(key)
            return result
        
        async def run_concurrent():
            tasks = [set_and_get(i) for i in range(10)]
            results = await asyncio.gather(*tasks)
            return results
        
        results = asyncio.run(run_concurrent())
        assert len(results) == 10
        for i, result in enumerate(results):
            assert result == {"index": i}
    
    def test_global_cache_instance(self):
        """Test global cache instance singleton"""
        cache1 = get_cache()
        cache2 = get_cache()
        assert cache1 is cache2  # Should be same instance
    
    def test_cache_with_large_data(self, cache, temp_file):
        """Test caching large data structures"""
        large_data = {
            "findings": [{"id": f"issue_{i}", "data": "x" * 1000} for i in range(100)],
            "summary": {"score": 85, "details": "y" * 5000}
        }
        
        key = cache.get_cache_key(temp_file, "large_test")
        assert cache.set(key, large_data)
        
        cached = cache.get(key)
        assert cached == large_data
    
    def test_cache_with_special_characters(self, cache):
        """Test cache handles special characters in file paths"""
        special_path = "path/with spaces/and-dashes/file_name.py"
        key = cache.get_cache_key(special_path, "test_op", "content")
        assert key  # Should generate valid key
        
        cache.set(key, {"test": "data"})
        assert cache.get(key) == {"test": "data"}
    
    def test_cache_error_handling(self, cache):
        """Test cache handles errors gracefully"""
        # Try to get hash of non-existent file
        hash_result = cache.get_file_hash("nonexistent_file.py")
        assert hash_result == ""  # Should return empty string, not crash
    
    def test_cache_persistence(self, temp_cache_dir, temp_file):
        """Test cache persists across cache instance recreations"""
        # Create first cache instance
        cache1 = FileCache(cache_dir=temp_cache_dir)
        key = cache1.get_cache_key(temp_file, "persist_test")
        cache1.set(key, {"persisted": True})
        
        # Create new cache instance (simulates restart)
        cache2 = FileCache(cache_dir=temp_cache_dir)
        
        # Should still have the data
        result = cache2.get(key)
        assert result == {"persisted": True}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

# Made with Bob
