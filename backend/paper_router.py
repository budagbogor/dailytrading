"""Paper-only broker router: no live execution, no broker fallback."""
from dataclasses import dataclass
from decimal import Decimal
from .broker_registry import select_broker
from .broker_adapters import PaperOrder, AlpacaPaperAdapter, IBKRPaperAdapter, positive

@dataclass(frozen=True)
class PaperTradeRequest:
    broker: str
    symbol: str
    side: str
    quantity: int
    limit_price: str
    sharia_verified: bool
    risk_approved: bool
    fresh_quote: bool
    max_notional_usd: str
    available_cash_usd: str
    reserved_cash_usd: str = '0'
    available_shares: int = 0

def prepare_paper_trade(request: PaperTradeRequest) -> dict:
    if not isinstance(request, PaperTradeRequest):
        raise TypeError('PaperTradeRequest required')
    selection = select_broker(request.broker, paper=True)
    if selection.broker not in ('alpaca', 'ibkr'):
        raise PermissionError('Unsupported paper broker')
    order = PaperOrder(symbol=request.symbol, side=request.side,
                       quantity=request.quantity, limit_price=request.limit_price,
                       market='US', sharia_verified=request.sharia_verified,
                       risk_approved=request.risk_approved,
                       fresh_quote=request.fresh_quote).validate()
    cap = positive(request.max_notional_usd, 'max_notional_usd')
    cash = positive(request.available_cash_usd, 'available_cash_usd')
    try:
        reserve = Decimal(str(request.reserved_cash_usd))
    except Exception:
        raise ValueError('invalid cash reserve') from None
    if not reserve.is_finite() or reserve < 0 or reserve > cash:
        raise ValueError('invalid cash reserve')
    notional = positive(order.limit_price, 'limit_price') * order.quantity
    if notional > cap:
        raise PermissionError('paper order exceeds notional cap')
    if order.side == 'buy' and notional > cash - reserve:
        raise PermissionError('paper order exceeds spendable cash')
    payload = (AlpacaPaperAdapter().prepare(order) if selection.broker == 'alpaca'
               else IBKRPaperAdapter().prepare(order))
    return {'broker': selection.broker, 'market': 'US', 'environment': 'paper',
            'status': 'PREPARED_NOT_SENT', 'live_order_enabled': False,
            'notional_usd': str(notional), 'payload': payload}
