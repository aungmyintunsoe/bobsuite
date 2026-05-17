import asyncio
import pytest
from unittest.mock import patch
from pathlib import Path
from mcp_server.lib.autodocs.core import AutoDocs

class TestAutoDocs:
    @pytest.mark.asyncio
    async def test_generate_api_docs(self):
        # Subject: AutoDocs.generate_docs
        # Scenario: Generating API documentation
        # Result: Returns valid API documentation string
        file_path = 'sample_code.py'
        doc_type = 'api'
        auto_docs = AutoDocs('mock_watsonx_client')
        result = await auto_docs.generate_docs(file_path, doc_type)
        assert 'API Documentation' in result
        assert Path(file_path) in result
        assert doc_type in result

    @pytest.mark.asyncio
    async def test_generate_full_docs(self):
        # Subject: AutoDocs.generate_docs
        # Scenario: Generating full documentation
        # Result: Returns valid full documentation string
        file_path = 'sample_code.py'
        doc_type = 'full'
        auto_docs = AutoDocs('mock_watsonx_client')
        result = await auto_docs.generate_docs(file_path, doc_type)
        for doc_name in [
            'API Documentation',
            'Quick Start Guide',
            'User Manual',
            'How-To Guide',
            'Tutorial',
            'Troubleshooting Guide',
            'Requirements Specification'
        ]:
            assert doc_name in result

    @pytest.mark.asyncio
    async def test_generate_invalid_doc_type(self):
        # Subject: AutoDocs.generate_docs
        # Scenario: Generating documentation with invalid type
        # Result: Returns error message
        file_path = 'sample_code.py'
        doc_type = 'invalid_type'
        auto_docs = AutoDocs('mock_watsonx_client')
        result = await auto_docs.generate_docs(file_path, doc_type)
        assert 'Error' in result

    @pytest.mark.asyncio
    async def test_generate_docs_with_cache(self):
        # Subject: AutoDocs.generate_docs
        # Scenario: Generating documentation with caching enabled
        # Result: Returns cached result on second call
        file_path = 'sample_code.py'
        doc_type = 'api'
        auto_docs = AutoDocs('mock_watsonx_client', enable_cache=True)
        result1 = await auto_docs.generate_docs(file_path, doc_type)
        result2 = await auto_docs.generate_docs(file_path, doc_type)
        assert result1 == result2

    @pytest.mark.asyncio
    async def test_generate_docs_with_error(self):
        # Subject: AutoDocs.generate_docs
        # Scenario: Generating documentation for non-existent file
        # Result: Returns error message
        file_path = 'non_existent_file.py'
        doc_type = 'api'
        auto_docs = AutoDocs('mock_watsonx_client')
        result = await auto_docs.generate_docs(file_path, doc_type)
        assert 'Error' in result

# Made with Bob
