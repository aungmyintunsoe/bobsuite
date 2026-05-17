"""
Comprehensive tests for all code quality improvements
Tests critical bug fixes, formatters, renderers, and constants
"""

import pytest
import asyncio
import time
import sys
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import tempfile

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from watsonx_client import WatsonxClient
from lib.utils.cache import FileCache
from lib.formatters import format_test_generation_response, format_visualizer_result
from lib.visualizer.renderers import save_mermaid_as_png, DiagramGenerationError
from lib.utils.constants import (
    HTTP_TIMEOUT_SECONDS,
    MAX_RETRY_ATTEMPTS,
    TOKEN_EXPIRY_BUFFER_SECONDS,
    DEFAULT_TOKEN_EXPIRY_SECONDS,
    CACHE_PATH_HASH_LENGTH
)


class TestTokenRefreshRaceCondition:
    """Test fix for token refresh race condition"""
    
    @pytest.mark.asyncio
    async def test_concurrent_token_refresh_uses_lock(self):
        """Test that concurrent token refreshes don't cause race conditions"""
        with patch.dict('os.environ', {'IBM_API_KEY': 'test_key', 'PROJECT_ID': 'test_project'}):
            client = WatsonxClient()
            
            # Mock the HTTP client to simulate token refresh
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'access_token': 'test_token',
                'expires_in': 3600
            }
            
            refresh_count = 0
            
            async def mock_post(*args, **kwargs):
                nonlocal refresh_count
                refresh_count += 1
                await asyncio.sleep(0.1)  # Simulate network delay
                return mock_response
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = mock_post
                
                # Trigger multiple concurrent token refreshes
                tasks = [client._get_token() for _ in range(10)]
                tokens = await asyncio.gather(*tasks)
                
                # All should get the same token
                assert all(token == 'test_token' for token in tokens)
                
                # Should only refresh once due to lock
                assert refresh_count == 1
    
    @pytest.mark.asyncio
    async def test_token_lock_exists(self):
        """Test that token lock is properly initialized"""
        with patch.dict('os.environ', {'IBM_API_KEY': 'test_key', 'PROJECT_ID': 'test_project'}):
            client = WatsonxClient()
            assert hasattr(client, '_token_lock')
            assert client._token_lock is not None


class TestRetryLogic:
    """Test retry logic with exponential backoff"""
    
    @pytest.mark.asyncio
    async def test_retry_on_network_error(self):
        """Test that network errors trigger retries"""
        with patch.dict('os.environ', {'IBM_API_KEY': 'test_key', 'PROJECT_ID': 'test_project'}):
            client = WatsonxClient()
            client._access_token = 'test_token'
            client._token_expires = time.time() + 3600
            
            attempt_count = 0
            
            from httpx import TimeoutException
            
            async def mock_post(*args, **kwargs):
                nonlocal attempt_count
                attempt_count += 1
                if attempt_count < 3:
                    raise TimeoutException("Network timeout")
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'results': [{'generated_text': 'Success!'}]
                }
                return mock_response
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = mock_post
                
                result = await client.generate_text("test prompt", max_retries=3)
                
                # Should have retried and succeeded
                assert result == 'Success!'
                assert attempt_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_on_5xx_errors(self):
        """Test that 5xx errors trigger retries"""
        with patch.dict('os.environ', {'IBM_API_KEY': 'test_key', 'PROJECT_ID': 'test_project'}):
            client = WatsonxClient()
            client._access_token = 'test_token'
            client._token_expires = time.time() + 3600
            
            attempt_count = 0
            
            async def mock_post(*args, **kwargs):
                nonlocal attempt_count
                attempt_count += 1
                mock_response = Mock()
                if attempt_count < 2:
                    mock_response.status_code = 503  # Service unavailable
                    mock_response.text = "Service temporarily unavailable"
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = {
                        'results': [{'generated_text': 'Success after retry!'}]
                    }
                return mock_response
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = mock_post
                
                result = await client.generate_text("test prompt", max_retries=3)
                
                assert result == 'Success after retry!'
                assert attempt_count == 2


class TestCacheKeyCollision:
    """Test fix for cache key collision"""
    
    def test_different_files_same_content_different_keys(self):
        """Test that files with same content but different paths have different cache keys"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = FileCache(cache_dir=temp_dir)
            
            content = "def hello(): return 'world'"
            
            # Same content, different paths
            key1 = cache.get_cache_key("/path/to/file1.py", "testop", content)
            key2 = cache.get_cache_key("/path/to/file2.py", "testop", content)
            
            # Keys should be different
            assert key1 != key2
            
            # Both should contain path hash (operation_pathhash_contenthash)
            # Note: operation name might contain underscores, so we check structure differently
            assert key1.startswith("testop_")
            assert key2.startswith("testop_")
            parts1 = key1.split('_')
            parts2 = key2.split('_')
            assert len(parts1) >= 3  # At least operation, path hash, content hash
            assert len(parts2) >= 3
    
    def test_cache_key_includes_path_hash(self):
        """Test that cache key includes path hash of correct length"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = FileCache(cache_dir=temp_dir)
            
            key = cache.get_cache_key("/test/path.py", "autodocs", "content")
            parts = key.split('_')
            
            assert len(parts) == 3
            assert parts[0] == "autodocs"
            assert len(parts[1]) == CACHE_PATH_HASH_LENGTH  # Path hash
            assert len(parts[2]) == 32  # Content hash (MD5)


class TestPNGGenerationErrorHandling:
    """Test PNG generation error handling improvements"""
    
    def test_empty_mermaid_code_raises_error(self):
        """Test that empty mermaid code raises DiagramGenerationError"""
        with pytest.raises(DiagramGenerationError, match="Empty mermaid code"):
            save_mermaid_as_png("", "output.md")
    
    def test_mermaid_code_with_only_wrapper_raises_error(self):
        """Test that mermaid code with only wrapper raises error"""
        with pytest.raises(DiagramGenerationError, match="Empty mermaid code"):
            save_mermaid_as_png("```mermaid\n```", "output.md")
    
    def test_network_error_raises_diagram_error(self):
        """Test that network errors are wrapped in DiagramGenerationError"""
        with patch('urllib.request.urlretrieve') as mock_retrieve:
            mock_retrieve.side_effect = Exception("Network error")
            
            with pytest.raises(DiagramGenerationError, match="Unexpected error"):
                save_mermaid_as_png("graph TD\n    A-->B", "output.md")
    
    def test_diagram_generation_error_is_exception(self):
        """Test that DiagramGenerationError is a proper exception"""
        assert issubclass(DiagramGenerationError, Exception)
        
        error = DiagramGenerationError("Test error")
        assert str(error) == "Test error"


class TestFormatters:
    """Test response formatters"""
    
    def test_format_network_test_response(self):
        """Test network test response formatting"""
        result = {
            'file_path': 'test.py',
            'language': 'python',
            'test_framework': 'pytest',
            'timestamp': '2026-05-17',
            'framework_justification': 'Best for Python',
            'dependencies': ['pytest', 'pytest-asyncio'],
            'execution_command': 'pytest test.py',
            'test_files': [{
                'filename': 'test_network.py',
                'description': 'Network tests',
                'content': 'def test_api(): pass'
            }],
            'performance_thresholds': {
                'response_time_ms': 100,
                'throughput_rps': 1000,
                'error_rate_percent': 1
            }
        }
        
        formatted = format_test_generation_response(result, 'network')
        
        assert '# Network Performance Tests Generated' in formatted
        assert 'test.py' in formatted
        assert 'pytest' in formatted
        assert 'Performance Thresholds' in formatted
        assert '100 ms' in formatted
    
    def test_format_unit_test_response(self):
        """Test unit test response formatting"""
        result = {
            'file_path': 'app.py',
            'language': 'python',
            'test_framework': 'unittest',
            'timestamp': '2026-05-17',
            'framework_justification': 'Standard library',
            'dependencies': [],
            'execution_command': 'python -m unittest',
            'test_files': [{
                'filename': 'test_app.py',
                'description': 'Unit tests',
                'content': 'def test_function(): pass'
            }],
            'mock_strategy': {
                'mocking_library': 'unittest.mock',
                'external_dependencies': ['database', 'api']
            },
            'test_coverage': {
                'test_count': 10,
                'units_tested': ['function1', 'function2']
            }
        }
        
        formatted = format_test_generation_response(result, 'unit')
        
        assert 'Unit Tests Generated' in formatted
        assert 'Steve Sanderson Principles' in formatted
        assert 'Mock Strategy' in formatted
        assert 'unittest.mock' in formatted
        assert 'Test Coverage' in formatted
    
    def test_format_visualizer_result(self):
        """Test visualizer result formatting"""
        result = {
            'markdown': '# Project Diagram\n\nSome content',
            'saved_to': '/path/to/diagram.md',
            'image_saved_to': '/path/to/diagram.png'
        }
        
        formatted = format_visualizer_result(result)
        
        assert '# Project Diagram' in formatted
        assert 'Blueprint saved to' in formatted
        assert '/path/to/diagram.md' in formatted
        assert 'Real Image saved to' in formatted
        assert '/path/to/diagram.png' in formatted


class TestConstants:
    """Test that constants are properly defined and used"""
    
    def test_http_constants_defined(self):
        """Test HTTP-related constants"""
        assert HTTP_TIMEOUT_SECONDS == 60.0
        assert MAX_RETRY_ATTEMPTS == 3
        assert isinstance(HTTP_TIMEOUT_SECONDS, float)
        assert isinstance(MAX_RETRY_ATTEMPTS, int)
    
    def test_token_constants_defined(self):
        """Test token-related constants"""
        assert TOKEN_EXPIRY_BUFFER_SECONDS == 60
        assert DEFAULT_TOKEN_EXPIRY_SECONDS == 3600
        assert isinstance(TOKEN_EXPIRY_BUFFER_SECONDS, int)
    
    def test_cache_constants_defined(self):
        """Test cache-related constants"""
        assert CACHE_PATH_HASH_LENGTH == 8
        assert isinstance(CACHE_PATH_HASH_LENGTH, int)
    
    def test_constants_are_used_in_watsonx_client(self):
        """Test that WatsonxClient uses constants"""
        with patch.dict('os.environ', {'IBM_API_KEY': 'test', 'PROJECT_ID': 'test'}):
            client = WatsonxClient()
            
            # Check that constants are imported and used
            # The function signature has: max_tokens, temperature, max_retries as defaults
            # Defaults are: (DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, MAX_RETRY_ATTEMPTS)
            import inspect
            sig = inspect.signature(client.generate_text)
            params = sig.parameters
            
            # Verify max_retries parameter exists and has correct default
            assert 'max_retries' in params
            assert params['max_retries'].default == MAX_RETRY_ATTEMPTS


class TestModuleSeparation:
    """Test that modules are properly separated"""
    
    def test_formatters_module_exists(self):
        """Test that formatters module exists and is importable"""
        from lib import formatters
        assert hasattr(formatters, 'format_test_generation_response')
        assert hasattr(formatters, 'format_visualizer_result')
    
    def test_renderers_module_exists(self):
        """Test that renderers module exists and is importable"""
        from lib.visualizer import renderers
        assert hasattr(renderers, 'save_mermaid_as_png')
        assert hasattr(renderers, 'DiagramGenerationError')
    
    def test_constants_module_exists(self):
        """Test that constants module exists and is importable"""
        from lib.utils import constants
        assert hasattr(constants, 'HTTP_TIMEOUT_SECONDS')
        assert hasattr(constants, 'MAX_RETRY_ATTEMPTS')
        assert hasattr(constants, 'DEFAULT_MAX_TOKENS')


class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.mark.asyncio
    async def test_watsonx_client_initialization(self):
        """Test WatsonxClient initializes with proper error handling"""
        # Test missing credentials
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="Missing required environment variables"):
                WatsonxClient()
    
    def test_cache_system_integration(self):
        """Test cache system works end-to-end"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = FileCache(cache_dir=temp_dir)
            
            # Create test file
            test_file = Path(temp_dir) / "test.py"
            test_file.write_text("def test(): pass")
            
            # Generate cache key
            key = cache.get_cache_key(str(test_file), "test_op")
            
            # Set and get
            test_data = {"result": "success"}
            cache.set(key, test_data)
            
            retrieved = cache.get(key)
            assert retrieved == test_data


def run_tests():
    """Run all tests"""
    pytest.main([__file__, '-v', '--tb=short', '-x'])


if __name__ == '__main__':
    run_tests()


# Made with Bob