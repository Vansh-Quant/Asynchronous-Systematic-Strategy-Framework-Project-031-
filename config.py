# config.py
"""
System Configuration Engine
Defines global constants, risk thresholds, and execution boundaries for the framework.
"""

SYSTEM_CONFIG = {
    "ASSET_UNIVERSE": ["BTC/USD", "ETH/USD", "SOL/USD"],
    "INITIAL_CAPITAL": 100000.00,
    "MAX_PORTFOLIO_EXPOSURE": 0.80,  # Never allow total exposure to exceed 80% of capital
    "MAX_SINGLE_TRADE_EXPOSURE": 0.25, # Strict 25% single-position ceiling
    "KELLY_FRACTION": 0.50,         # Half-Kelly adjustment for defensive sizing
    "DATA_STREAM_DELAY": 0.5        # Simulated async delay in seconds (speed simulation)
}