import unittest
from backend.paper_router import PaperTradeRequest, prepare_paper_trade

class PaperHoldingsTests(unittest.TestCase):
    def request(self, shares):
        return PaperTradeRequest(broker='alpaca',symbol='AAPL',side='sell',quantity=2,
            limit_price='100',sharia_verified=True,risk_approved=True,fresh_quote=True,
            max_notional_usd='1000',available_cash_usd='1000',available_shares=shares)
    def test_sufficient_holdings(self):
        r=prepare_paper_trade(self.request(2))
        self.assertEqual(r['status'],'PREPARED_NOT_SENT')
        self.assertFalse(r['live_order_enabled'])
    def test_missing_holdings(self):
        with self.assertRaises(PermissionError): prepare_paper_trade(self.request(0))
    def test_insufficient_holdings(self):
        with self.assertRaises(PermissionError): prepare_paper_trade(self.request(1))
    def test_invalid_holdings(self):
        for shares in (-1,True):
            with self.subTest(shares=shares), self.assertRaises(ValueError):
                prepare_paper_trade(self.request(shares))
