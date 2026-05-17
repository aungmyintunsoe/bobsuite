import asyncio
from unittest.mock import patch, MagicMock
from mcp_server.lib.qa_sentry.core import QASentry

class TestCoreScanning:
    def setup_method(self):
        self.watsonx_mock = MagicMock()
        self.sentry = QASentry(self.watsonx_mock)

    @patch('mcp_server.lib.qa_sentry.core.read_file_safe')
    def test_scan_code_reads_file_safely(self, mock_read):
        mock_read.return_value = ('def foo():\n    pass', None)
        result = asyncio.run(self.sentry.scan_code('dummy.py'))
        assert result['success']
        assert result['language'] == 'python'

    @patch('mcp_server.lib.qa_sentry.core.detect_language')
    def test_scan_code_handles_unknown_language(self, mock_detect):
        mock_detect.return_value = 'Unknown'
        result = asyncio.run(self.sentry.scan_code('dummy.py'))
        assert result['language'] == 'text'

    @patch('mcp_server.lib.qa_sentry.core.finder_pass')
    @patch('mcp_server.lib.qa_sentry.core.critic_pass')
    def test_scan_code_two_pass_debate(self, mock_critic, mock_finder):
        mock_finder.return_value = {'summary': {'health_score': 80}, 'findings': []}
        mock_critic.return_value = {'summary': {'health_score': 85}, 'findings': []}
        result = asyncio.run(self.sentry.scan_code('dummy.py'))
        assert result['summary']['health_score'] == 85

    @patch('mcp_server.lib.qa_sentry.core.apply_auto_fixes')
    def test_scan_code_auto_fix_application(self, mock_fix):
        mock_fix.return_value = {'fixed': True}
        result = asyncio.run(self.sentry.scan_code('dummy.py', auto_fix=True))
        assert result['auto_fix_applied']['fixed']

    def test_generate_unit_tests_delegates(self):
        result = asyncio.run(self.sentry.generate_unit_tests('dummy.py'))
        assert isinstance(result, dict)
        assert 'tests' in result

    def test_generate_network_tests_delegates(self):
        result = asyncio.run(self.sentry.generate_network_performance_tests('dummy.py'))
        assert isinstance(result, dict)
        assert 'tests' in result

# Made with Bob
