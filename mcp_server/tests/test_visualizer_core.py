import asyncio
from unittest.mock import AsyncMock, patch
from pathlib import Path
import pytest
from mcp_server.lib.visualizer.core import VisualizerEngine

class TestVisualizerEngine:
    @pytest.fixture
    def engine(self):
        # Mock WatsonX client for isolation
        watsonx_client = AsyncMock()
        return VisualizerEngine(watsonx_client)

    @pytest.mark.asyncio
    async def test_generate_dependency_chain_success(self, engine):
        # S: VisualizerEngine.generate_dependency_chain
        # S: _analyze_dependencies
        # R: Returns successful response with modules, edges, external
        result = await engine.generate_dependency_chain("./test_project")
        assert result["success"]
        assert result["diagram_type"] == "dependency_chain"
        assert result["stats"]["total_modules"] > 0
        assert result["stats"]["total_dependencies"] > 0

    @pytest.mark.asyncio
    async def test_generate_dependency_chain_external(self, engine):
        # S: VisualizerEngine.generate_dependency_chain
        # S: _analyze_dependencies
        # R: Includes external flag handling
        result = await engine.generate_dependency_chain(
            "./test_project", include_external=True
        )
        assert result["success"]
        assert result["stats"]["external_deps"] > 0

    @pytest.mark.asyncio
    async def test_generate_feature_flow_success(self, engine):
        # S: VisualizerEngine.generate_feature_flow
        # S: _analyze_features_with_ai
        # S: _create_feature_flow_mermaid
        # R: Returns successful response with mermaid diagram
        result = await engine.generate_feature_flow("./test_project", feature_name="FeatureX")
        assert result["success"]
        assert result["diagram_type"] == "feature_flow"
        assert result["mermaid"].startswith("```mermaid")

    @pytest.mark.asyncio
    async def test_generate_project_concept_success(self, engine):
        # S: VisualizerEngine.generate_project_concept
        # S: _analyze_project_concept_with_ai
        # S: _create_concept_mermaid
        # R: Returns successful response with mermaid diagram
        result = await engine.generate_project_concept("./test_project")
        assert result["success"]
        assert result["diagram_type"] == "project_concept"
        assert result["mermaid"].startswith("```mermaid")

    @patch("mcp_server.lib.visualizer.core.read_file_safe")
    def test_parse_imports_success(self, mock_read, engine):
        # S: VisualizerEngine._parse_imports
        # R: Correctly parses imports from content
        mock_read.return_value = "from lib.utils import detect_language\nimport json"
        imports = engine._parse_imports(
            Path("dummy.py"), local_roots={"mcp_server"}
        )
        assert len(imports) == 2
        assert imports[0]["module"] == "lib.utils"
        assert imports[1]["module"] == "json"

    @patch("mcp_server.lib.visualizer.core.read_file_safe")
    def test_parse_imports_regex_fallback(self, mock_read, engine):
        # S: VisualizerEngine._parse_imports_regex (fallback)
        # R: Parses imports when AST fails
        mock_read.return_value = "from .module import func\nimport os, sys"
        imports = engine._parse_imports_regex(
            mock_read.return_value, local_roots={"mcp_server"}
        )
        assert len(imports) == 3
        assert imports[0]["module"] == ".module"
        assert imports[1]["module"] == "os"

    def test_get_module_name(self, engine):
        # S: VisualizerEngine._get_module_name
        # R: Correctly computes module names from paths
        assert engine._get_module_name(
            Path("tests/unit/core.py"), Path("mcp_server")
        ) == "tests.unit.core"
        assert engine._get_module_name(
            Path("mcp_server/lib/visualizer/core.py"), Path("mcp_server")
        ) == "lib.visualizer.core"

    def test_mocking_external_services(self, engine):
        # S: External service mocking strategy
        # R: Demonstrates proper isolation using AsyncMock
        with patch(
            "mcp_server.lib.visualizer.core.watsonx_client",
            new_callable=AsyncMock,
        ) as mock_client:
            engine.watsonx = mock_client
            # Any async method call on watsonx will be mocked
            assert asyncio.run(engine._analyze_features_with_ai(Path("/")))

    def test_error_handling(self, engine):
        # S: VisualizerEngine.generate_dependency_chain error handling
        # R: Returns proper error structure on failure
        result = engine.generate_dependency_chain("/non/existent/path")
        assert not result["success"]
        assert "does not exist" in result["error"]

# Made with Bob
