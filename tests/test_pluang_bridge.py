import unittest
from backend.pluang_bridge import (OFFICIAL_MCP_URL, PluangPolicy, integration_status,
                                    validate_endpoint, validate_research_request)

class PluangBridgeTests(unittest.TestCase):
    def test_official_url(self):
        self.assertEqual(validate_endpoint(OFFICIAL_MCP_URL), OFFICIAL_MCP_URL)

    def test_lookalikes_rejected(self):
        for url in ('http://mcp.pluang.com/mcp', 'https://mcp.pluang.com.evil.test/mcp',
                    'https://mcp.pluang.com/mcp?token=secret', 'https://mcp.pluang.com/mcp/',
                    'https://mcp.pluang.com/mcp#frag'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_endpoint(url)

    def test_read_only_default(self):
        policy = PluangPolicy()
        self.assertTrue(policy.read_only)
        self.assertFalse(policy.allow_order_execution)
        self.assertFalse(policy.allow_order_proposals)

    def test_disconnected_status_is_honest(self):
        state = integration_status()
        self.assertFalse(state['read_only_enabled'])
        self.assertFalse(state['order_execution_enabled'])

    def test_cannot_verify_tools_before_oauth(self):
        with self.assertRaises(ValueError):
            integration_status(tools_verified=True)

    def test_research_requires_sharia(self):
        with self.assertRaises(ValueError):
            validate_research_request('BBCA', False)

    def test_research_never_executes(self):
        self.assertFalse(validate_research_request('BBCA', True)['execution'])

    def test_ticker_validation(self):
        for ticker in ('bbca', 'BBCA1', 'ＡＢＣＤ', 'AB C'):
            with self.subTest(ticker=ticker), self.assertRaises(ValueError):
                validate_research_request(ticker, True)

    def test_reject_non_indonesian_asset(self):
        with self.assertRaises(ValueError):
            validate_research_request('BBCA', True, 'US_STOCK')
