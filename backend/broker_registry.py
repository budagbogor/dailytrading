"""Broker selection policy: Pluang default; IBKR and Alpaca optional."""
from dataclasses import dataclass

DEFAULT_BROKER = "pluang"
SUPPORTED_BROKERS = ("pluang", "ibkr", "alpaca")

@dataclass(frozen=True)
class BrokerSelection:
    broker: str = DEFAULT_BROKER
    market: str = "ID"
    execution_mode: str = "assisted"
    live_order_enabled: bool = False
    paper_order_enabled: bool = False
    confirmation_required: bool = True

def select_broker(broker=None, *, paper=False):
    if broker is None:
        broker = DEFAULT_BROKER
    if not isinstance(broker, str) or broker not in SUPPORTED_BROKERS:
        raise ValueError("Unsupported broker; no fallback to live execution")
    if type(paper) is not bool:
        raise ValueError("paper must be a boolean")
    if broker == "pluang":
        if paper:
            raise ValueError("Pluang MCP paper order execution is not verified")
        return BrokerSelection()
    return BrokerSelection(broker=broker, market="US",
                           execution_mode="paper_preparation" if paper else "research_only")

def broker_catalog():
    return {"default": DEFAULT_BROKER, "choices": [
        {"id": "pluang", "market": "ID", "mode": "assisted",
         "selected_by_default": True, "live_order_enabled": False,
         "requires_manual_approval": True},
        {"id": "ibkr", "market": "US", "mode": "paper_preparation",
         "selected_by_default": False, "live_order_enabled": False,
         "requires_manual_approval": True},
        {"id": "alpaca", "market": "US", "mode": "paper_preparation",
         "selected_by_default": False, "live_order_enabled": False,
         "requires_manual_approval": True},
    ]}
