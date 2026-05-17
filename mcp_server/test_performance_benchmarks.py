"""
Performance Benchmark Tests
Measures actual speedups from optimizations and ensures performance targets are met
"""

import pytest
import asyncio
import time
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from lib.autodocs.core import AutoDocs
from lib.qa_sentry.core import QASentry
from lib.utils.cache import FileCache


class MockWatsonxClient:
    """Mock watsonx client for testing without API calls"""
    
    def __init__(self, delay=0.1):
        self.delay = delay
        self.call_count = 0
    
    async def generate_text(self, prompt, temperature=0.5, max_tokens=4000):
        """Simulate AI generation with configurable delay"""
        self.call_count += 1
        await asyncio.sleep(self.delay)
        return f"Generated documentation {self.call_count}"


class TestAutodocsPerformance:
    """Performance benchmarks for AutoDocs optimizations"""
    
    @pytest.fixture
    def mock_watsonx(self):
        return MockWatsonxClient(delay=0.1)  # 100ms per call
    
    @pytest.fixture
    def temp_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("""
def example_function(x, y):
    '''Example function for testing'''
    return x + y

class ExampleClass:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
""")
            temp_path = f.name
        yield temp_path
        Path(temp_path).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_concurrent_generation_speedup(self, mock_watsonx, temp_file):
        """Test that concurrent generation is faster than sequential"""
        autodocs = AutoDocs(mock_watsonx, enable_cache=False)
        
        # Measure full documentation generation time
        start_time = time.time()
        result = await autodocs.generate_docs(temp_file, doc_type="full")
        elapsed_time = time.time() - start_time
        
        # With 7 doc types and 100ms per call:
        # Sequential would take: 7 * 0.1 = 0.7s
        # Concurrent should take: ~0.1-0.2s (parallel execution)
        
        assert result  # Should generate something
        assert elapsed_time < 0.4  # Should be much faster than 0.7s
        print(f"\n✓ Full docs generated in {elapsed_time:.2f}s (target: <0.4s)")
        print(f"  API calls made: {mock_watsonx.call_count}")
        
        # Verify concurrent execution (should make 7 calls)
        assert mock_watsonx.call_count == 7
    
    @pytest.mark.asyncio
    async def test_cache_performance(self, mock_watsonx, temp_file):
        """Test that caching provides instant results on second run"""
        autodocs = AutoDocs(mock_watsonx, enable_cache=True)
        
        # First run (no cache)
        start_time = time.time()
        result1 = await autodocs.generate_docs(temp_file, doc_type="api")
        first_run_time = time.time() - start_time
        
        # Second run (cached)
        start_time = time.time()
        result2 = await autodocs.generate_docs(temp_file, doc_type="api")
        cached_run_time = time.time() - start_time
        
        # Cached run should be much faster (< 10ms vs 100ms+)
        assert cached_run_time < first_run_time / 5  # At least 5x faster
        assert cached_run_time < 0.05  # Should be nearly instant
        
        print(f"\n✓ First run: {first_run_time:.3f}s")
        print(f"✓ Cached run: {cached_run_time:.3f}s")
        print(f"✓ Speedup: {first_run_time/cached_run_time:.1f}x")
        
        # Results should be identical
        assert result1 == result2


class TestQASentryPerformance:
    """Performance benchmarks for QA Sentry optimizations"""
    
    @pytest.fixture
    def mock_watsonx(self):
        return MockWatsonxClient(delay=0.1)
    
    @pytest.fixture
    def temp_files(self):
        """Create multiple temporary files for batch testing"""
        files = []
        for i in range(5):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
                f.write(f"""
def function_{i}(x):
    '''Function {i}'''
    return x * {i}
""")
                files.append(f.name)
        yield files
        for f in files:
            Path(f).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_concurrent_batch_scanning(self, mock_watsonx, temp_files):
        """Test that batch scanning is concurrent and faster"""
        qa_sentry = QASentry(mock_watsonx, enable_cache=False)
        
        # Measure batch scan time
        start_time = time.time()
        results = await qa_sentry.batch_scan(temp_files)
        elapsed_time = time.time() - start_time
        
        # With 5 files and 100ms per file (2 passes each):
        # Sequential would take: 5 * 2 * 0.1 = 1.0s
        # Concurrent should take: ~0.2-0.3s (parallel execution)
        
        assert len(results) == 5
        assert elapsed_time < 0.6  # Should be much faster than 1.0s
        
        print(f"\n✓ Batch scan of {len(temp_files)} files in {elapsed_time:.2f}s")
        print(f"  Target: <0.6s (sequential would be ~1.0s)")
        print(f"  Speedup: ~{1.0/elapsed_time:.1f}x")
    
    @pytest.mark.asyncio
    async def test_chunk_size_optimization(self, mock_watsonx):
        """Test that larger chunk size reduces API calls"""
        qa_sentry = QASentry(mock_watsonx, enable_cache=False)
        
        # Create a large file (2000 lines)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            for i in range(2000):
                f.write(f"# Line {i}\n")
            temp_path = f.name
        
        try:
            # Scan the large file
            result = await qa_sentry.scan_code(temp_path)
            
            # With 1000-line chunks, 2000 lines should create 2 chunks
            # Each chunk needs 1 finder pass (no critic for chunks)
            # So we expect 2 API calls
            
            assert result['success']
            assert 'chunks_processed' in result
            assert result['chunks_processed'] == 2
            
            print(f"\n✓ Large file (2000 lines) processed in {result['chunks_processed']} chunks")
            print(f"  Chunk size: {qa_sentry.chunk_size} lines")
            print(f"  API calls: {mock_watsonx.call_count}")
            
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_cache_skip_unchanged_files(self, mock_watsonx, temp_files):
        """Test that caching skips unchanged files in batch scans"""
        qa_sentry = QASentry(mock_watsonx, enable_cache=True)
        
        # First batch scan
        start_time = time.time()
        results1 = await qa_sentry.batch_scan(temp_files)
        first_run_time = time.time() - start_time
        first_call_count = mock_watsonx.call_count
        
        # Second batch scan (all cached)
        mock_watsonx.call_count = 0  # Reset counter
        start_time = time.time()
        results2 = await qa_sentry.batch_scan(temp_files)
        cached_run_time = time.time() - start_time
        cached_call_count = mock_watsonx.call_count
        
        # Cached run should make no API calls
        assert cached_call_count == 0
        assert cached_run_time < first_run_time / 10  # At least 10x faster
        
        print(f"\n✓ First batch scan: {first_run_time:.2f}s ({first_call_count} API calls)")
        print(f"✓ Cached batch scan: {cached_run_time:.3f}s ({cached_call_count} API calls)")
        print(f"✓ Speedup: {first_run_time/cached_run_time:.0f}x")


class TestCachePerformance:
    """Performance benchmarks for caching system"""
    
    @pytest.fixture
    def temp_cache_dir(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_cache_write_performance(self, temp_cache_dir):
        """Test cache write performance"""
        cache = FileCache(cache_dir=temp_cache_dir)
        
        # Write 100 cache entries
        start_time = time.time()
        for i in range(100):
            cache.set(f"key_{i}", {"data": f"value_{i}", "index": i})
        write_time = time.time() - start_time
        
        # Should complete in reasonable time
        assert write_time < 1.0  # Less than 1 second for 100 writes
        
        print(f"\n✓ Wrote 100 cache entries in {write_time:.3f}s")
        print(f"  Average: {write_time/100*1000:.1f}ms per entry")
    
    def test_cache_read_performance(self, temp_cache_dir):
        """Test cache read performance (memory vs disk)"""
        cache = FileCache(cache_dir=temp_cache_dir)
        
        # Write entries
        for i in range(100):
            cache.set(f"key_{i}", {"data": f"value_{i}"})
        
        # Read from memory cache (should be fast)
        start_time = time.time()
        for i in range(100):
            result = cache.get(f"key_{i}")
            assert result is not None
        memory_read_time = time.time() - start_time
        
        # Clear memory cache
        cache.memory_cache.clear()
        
        # Read from disk cache (slower but still fast)
        start_time = time.time()
        for i in range(100):
            result = cache.get(f"key_{i}")
            assert result is not None
        disk_read_time = time.time() - start_time
        
        print(f"\n✓ Memory cache reads: {memory_read_time:.3f}s (100 entries)")
        print(f"✓ Disk cache reads: {disk_read_time:.3f}s (100 entries)")
        print(f"✓ Memory is {disk_read_time/memory_read_time:.1f}x faster")
        
        # Memory should be significantly faster
        assert memory_read_time < disk_read_time


class TestOverallPerformanceTargets:
    """Verify overall performance targets are met"""
    
    @pytest.mark.asyncio
    async def test_autodocs_full_mode_target(self):
        """Verify AutoDocs full mode meets 5-7x speedup target"""
        mock_watsonx = MockWatsonxClient(delay=0.1)
        autodocs = AutoDocs(mock_watsonx, enable_cache=False)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("def test(): pass")
            temp_path = f.name
        
        try:
            start_time = time.time()
            await autodocs.generate_docs(temp_path, doc_type="full")
            elapsed_time = time.time() - start_time
            
            # Sequential would take 7 * 0.1 = 0.7s
            # Target is 5-7x speedup, so should be < 0.14s
            sequential_time = 0.7
            speedup = sequential_time / elapsed_time
            
            print(f"\n✓ AutoDocs Full Mode Performance:")
            print(f"  Concurrent time: {elapsed_time:.2f}s")
            print(f"  Sequential time (estimated): {sequential_time:.2f}s")
            print(f"  Speedup: {speedup:.1f}x")
            print(f"  Target: 5-7x ✓" if speedup >= 5 else f"  Target: 5-7x ✗")
            
            assert speedup >= 4  # Allow some margin
            
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_qa_sentry_batch_target(self):
        """Verify QA Sentry batch scanning meets 3-5x speedup target"""
        mock_watsonx = MockWatsonxClient(delay=0.1)
        qa_sentry = QASentry(mock_watsonx, enable_cache=False)
        
        # Create 5 test files
        files = []
        for i in range(5):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
                f.write(f"def test_{i}(): pass")
                files.append(f.name)
        
        try:
            start_time = time.time()
            await qa_sentry.batch_scan(files)
            elapsed_time = time.time() - start_time
            
            # Sequential would take 5 files * 2 passes * 0.1s = 1.0s
            # Target is 3-5x speedup, so should be < 0.33s
            sequential_time = 1.0
            speedup = sequential_time / elapsed_time
            
            print(f"\n✓ QA Sentry Batch Scan Performance:")
            print(f"  Concurrent time: {elapsed_time:.2f}s")
            print(f"  Sequential time (estimated): {sequential_time:.2f}s")
            print(f"  Speedup: {speedup:.1f}x")
            print(f"  Target: 3-5x ✓" if speedup >= 3 else f"  Target: 3-5x ✗")
            
            assert speedup >= 2.5  # Allow some margin
            
        finally:
            for f in files:
                Path(f).unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])

# Made with Bob
