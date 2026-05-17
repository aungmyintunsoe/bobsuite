import asyncio
import time
import httpx
from typing import Dict, Any

import pytest
from pytest_asyncio import fixture
from pytest_benchmark.fixture import BenchmarkFixture

from mcp_server.watsonx_client import WatsonxClient

@pytest.fixture(scope="session")
async def client() -> WatsonxClient:
    """Create a single client instance for all tests."""
    return WatsonxClient()

@pytest.mark.asyncio
async def test_api_connection(client: WatsonxClient) -> None:
    """Verify successful API connection and token retrieval."""
    token = await client._get_token()
    assert token, "Token should not be empty"

@pytest.mark.asyncio
async def test_generate_text(client: WatsonxClient) -> None:
    """Test basic text generation with valid input."""
    response = await client.generate_text(prompt="Hello, world!")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_generate_text_timeout(client: WatsonxClient) -> None:
    """Test timeout scenario by setting a very low timeout."""
    with pytest.raises(httpx.TimeoutException):
        async with httpx.AsyncClient(timeout=0.001) as client:
            await client.generate_text(prompt="Timeout test", max_retries=0)

@pytest.mark.asyncio
async def test_rate_limiting(client: WatsonxClient) -> None:
    """Test behavior when hitting rate limits."""
    # Simulate rate limit by making many rapid requests
    tasks = [client.generate_text(prompt="Rate limit test") for _ in range(10)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    rate_limited = sum(isinstance(r, httpx.HTTPError) and r.response.status_code == 429 for r in results)
    assert rate_limited <= 1, "Only one request should hit rate limit"

@pytest.mark.asyncio
async def test_concurrent_requests(client: WatsonxClient) -> None:
    """Test concurrent request handling."""
    prompts = [f"Prompt {i}" for i in range(20)]
    tasks = [client.generate_text(prompt=p) for p in prompts]
    results = await asyncio.gather(*tasks)
    assert len(results) == len(prompts)
    for result in results:
        assert isinstance(result, str)

@pytest.mark.asyncio
async def test_error_handling(client: WatsonxClient) -> None:
    """Test error handling for invalid model ID."""
    with pytest.raises(RuntimeError):
        await client.generate_text(prompt="Error test", model_id="invalid-model-id")

@pytest.mark.asyncio
async def test_performance(benchmark: BenchmarkFixture, client: WatsonxClient) -> None:
    """Benchmark text generation performance."""
    result = await benchmark.async_run(client.generate_text, prompt="Performance test")
    assert result.success

@pytest.mark.asyncio
async def test_large_payload(client: WatsonxClient) -> None:
    """Test generation with large payload."""
    large_prompt = " ".join(["Test sentence " for _ in range(1000)])
    result = await client.generate_text(prompt=large_prompt, max_tokens=500)
    assert len(result.split()) <= 500

# Made with Bob
