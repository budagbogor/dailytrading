"""Pluang official MCP integration boundary. No orders or credentials."""
from dataclasses import dataclass
from urllib.parse import urlsplit

OFFICIAL_MCP_URL = "https://mcp.pluang.com/mcp"
SUPPORTED_ASSETS = ("ID_STOCK", "US_STOCK", "CRYPTO_SPOT")

@dataclass(frozen=True)
class PluangPolicy:
    read_only: bool = True
    allow_order_proposals: bool = False
    allow_order_execution: bool = False
    require_sharia_verification: bool = True
    require_user_confirmation: bool = True

def validate_endpoint(url: str) -> str:
    if not isinstance(url, str) or url != OFFICIAL_MCP_URL:
        raise ValueError("Only the published official Pluang MCP URL is permitted")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "mcp.pluang.com":
        raise ValueError("Invalid Pluang MCP endpoint")
    return url

def integration_status(*, oauth_completed: bool = False, tools_verified: bool = False) -> dict:
    if tools_verified and not oauth_completed:
        raise ValueError("MCP tools cannot be verified before OAuth")
    return {
        "provider": "pluang", "protocol": "MCP",
        "official_endpoint": OFFICIAL_MCP_URL,
        "oauth_completed": oauth_completed, "tools_verified": tools_verified,
        "read_only_enabled": oauth_completed and tools_verified,
        "order_proposals_enabled": False, "order_execution_enabled": False,
        "sharia_screening_required": True,
        "next_step": ("Discover permitted read-only tools after OAuth" if oauth_completed
                      else "Authorize via official Pluang login in an MCP-capable client"),
    }

def validate_research_request(ticker: str, sharia_verified: bool, asset: str = "ID_STOCK") -> dict:
    if not isinstance(ticker, str) or not ticker.isascii() or not ticker.isalpha() or len(ticker) != 4 or ticker != ticker.upper():
        raise ValueError("Indonesian stock ticker must be four uppercase ASCII letters")
    if asset != "ID_STOCK":
        raise ValueError("QuantSyariah Pluang research currently supports Indonesian stocks only")
    if sharia_verified is not True:
        raise ValueError("Current official Sharia status must be verified first")
    return {"ticker": ticker, "asset": asset, "action": "research_only", "execution": False}
