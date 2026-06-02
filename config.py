# config.py
"""
System Configuration Matrix
Comprehensive, multi-generation compatibility configuration wrapper.
"""

# --- BASE DATA VARIABLES ---
INITIAL_CAPITAL_POOL = 250000.00   # $250k Scaled account size
MAX_PORTFOLIO_EXPOSURE = 0.75      # 75% Global leverage ceiling
MAX_SINGLE_TRADE_EXPOSURE = 0.25   # 25% Maximum single position size
KELLY_FRACTION_MULTIPLIER = 0.50   # Half-Kelly sizing baseline

FLAT_TICKET_COMMISSION = 1.50      # $1.50 flat per ticket fee
MAX_SLIPPAGE_BPS = 0.0012          # 12 basis points maximum slippage scale

DATA_STREAM_DELAY = 0.10           # 100ms async stream pause interval
ASSET_UNIVERSE = ["BTC/USD", "ETH/USD", "SOL/USD"]


# --- THE MASTER BACKWARD-COMPATIBILITY DICTIONARY ---
# Maps every variant, shorthand, and legacy string lookup keys to prevent all KeyErrors.
SYSTEM_CONFIG = {
    # Capital allocations variants
    "INITIAL_CAPITAL": INITIAL_CAPITAL_POOL,
    "INITIAL_CAPITAL_POOL": INITIAL_CAPITAL_POOL,
    "CAPITAL_POOL": INITIAL_CAPITAL_POOL,
    
    # Global exposure ceilings variants
    "MAX_PORTFOLIO_EXPOSURE": MAX_PORTFOLIO_EXPOSURE,
    "PORTFOLIO_EXPOSURE_CAP": MAX_PORTFOLIO_EXPOSURE,
    
    # Position limits variants
    "MAX_SINGLE_TRADE_EXPOSURE": MAX_SINGLE_TRADE_EXPOSURE,
    "SINGLE_TRADE_LIMIT": MAX_SINGLE_TRADE_EXPOSURE,
    
    # Kelly fraction metrics variants
    "KELLY_FRACTION": KELLY_FRACTION_MULTIPLIER,
    "KELLY_FRACTION_MULTIPLIER": KELLY_FRACTION_MULTIPLIER,
    "KELLY_FRACTION_MULT": KELLY_FRACTION_MULTIPLIER,
    
    # Execution friction models variants (Comprehensive Coverage)
    "FLAT_TICKET_COMMISSION": FLAT_TICKET_COMMISSION,
    "COMMISSION": FLAT_TICKET_COMMISSION,
    "BROKER_COMMISSION_PER_TRADE": FLAT_TICKET_COMMISSION,   # Fixed risk_manager.py lookup
    "COMMISSION_PER_TRADE": FLAT_TICKET_COMMISSION,
    
    # Slippage metrics variants
    "MAX_SLIPPAGE_BPS": MAX_SLIPPAGE_BPS,
    "SLIPPAGE_BPS": MAX_SLIPPAGE_BPS,
    "MAX_SLIPPAGE": MAX_SLIPPAGE_BPS,
    
    # Environment boundaries variants
    "ASSET_UNIVERSE": ASSET_UNIVERSE,
    "UNIVERSE": ASSET_UNIVERSE,
    "DATA_STREAM_DELAY": DATA_STREAM_DELAY,
    "STREAM_DELAY": DATA_STREAM_DELAY
}