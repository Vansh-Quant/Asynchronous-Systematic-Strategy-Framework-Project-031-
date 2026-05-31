# risk_manager.py
from config import SYSTEM_CONFIG

class RiskManager:
    def __init__(self):
        self.available_capital = SYSTEM_CONFIG["INITIAL_CAPITAL"]
        self.max_portfolio_exposure = SYSTEM_CONFIG["MAX_PORTFOLIO_EXPOSURE"]
        self.max_single_trade_exposure = SYSTEM_CONFIG["MAX_SINGLE_TRADE_EXPOSURE"]
        self.kelly_fraction = SYSTEM_CONFIG["KELLY_FRACTION"]
        
        self.current_allocated_capital = 0.0
        # New: Tracking ledger for active open positions
        self.active_positions = {} 

    def calculate_allocation(self, signal: dict) -> float:
        asset = signal["asset"]
        direction = signal["direction"]
        price = signal["price"]

        # Handle Exit Signals: Liquidate position and release exposure limits
        if direction == "EXIT":
            if asset in self.active_positions:
                pos = self.active_positions.pop(asset)
                # Simple PnL calculation: (Current Price / Entry Price - 1) * Allocated Capital
                # For simulation, we assume entry direction was long for simplicity
                return_pct = (price / pos["entry_price"]) - 1 if pos["direction"] == "LONG" else 1 - (price / pos["entry_price"])
                pnl = pos["allocated_amount"] * return_pct
                
                # Release capital back into the pool
                self.available_capital += pnl
                self.current_allocated_capital -= pos["allocated_amount"]
                
                print(f"[RISK LIQUIDATION] Exited {asset} at ${price:.2f} | PnL: ${pnl:,.2f} | Capital Pool Restored")
            return 0.0

        # Block duplicate entries if we are already exposed to this asset
        if asset in self.active_positions:
            return 0.0

        # Core Kelly Math
        p, b = 0.54, 1.2
        q = 1.0 - p
        raw_kelly = ((b * p) - q) / b
        target_allocation = self.available_capital * (raw_kelly * self.kelly_fraction)
        
        # Enforce ceilings
        single_trade_ceiling = self.available_capital * self.max_single_trade_exposure
        if target_allocation > single_trade_ceiling:
            target_allocation = single_trade_ceiling
            
        portfolio_ceiling = SYSTEM_CONFIG["INITIAL_CAPITAL"] * self.max_portfolio_exposure
        if self.current_allocated_capital + target_allocation > portfolio_ceiling:
            target_allocation = portfolio_ceiling - self.current_allocated_capital
            
        if target_allocation < 0.01:
            return 0.0
            
        return round(target_allocation, 2)

    def update_allocated_risk(self, asset: str, direction: str, price: float, amount: float):
        """Registers a newly opened position into the registry."""
        self.current_allocated_capital += amount
        self.active_positions[asset] = {
            "direction": direction,
            "entry_price": price,
            "allocated_amount": amount
        }