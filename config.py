# config.py
"""
System Configuration Engine - Friction Upgrade
Defines global constants, risk thresholds, and execution friction parameters.
"""

SYSTEM_CONFIG = {
    "ASSET_UNIVERSE": ["BTC/USD", "ETH/USD", "SOL/USD"],
    "INITIAL_CAPITAL": 100000.00,
    "MAX_PORTFOLIO_EXPOSURE": 0.80,    # 80% maximum total risk cap
    "MAX_SINGLE_TRADE_EXPOSURE": 0.25,   # 25% single-position ceiling
    "KELLY_FRACTION": 0.50,           # Half-Kelly adjustment
    "DATA_STREAM_DELAY": 0.5,         # Loop speed simulation
    
    # --- REAL-WORLD EXECUTION FRICTION CONSTANTS ---
    "BROKER_COMMISSION_PER_TRADE": 2.00,  # Flat $2.00 fee per execution ticket
    "MAX_SLIPPAGE_BPS": 15.0              # Max execution slippage of 15 Basis Points (0.15%)
}