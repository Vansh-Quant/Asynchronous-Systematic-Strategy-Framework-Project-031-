# risk_manager.py
import random
from config import SYSTEM_CONFIG

class RiskManager:
    def __init__(self):
        self.available_capital = SYSTEM_CONFIG["INITIAL_CAPITAL"]
        self.max_portfolio_exposure = SYSTEM_CONFIG["MAX_PORTFOLIO_EXPOSURE"]
        self.max_single_trade_exposure = SYSTEM_CONFIG["MAX_SINGLE_TRADE_EXPOSURE"]
        self.kelly_fraction = SYSTEM_CONFIG["KELLY_FRACTION"]
        
        self.current_allocated_capital = 0.0
        self.active_positions = {} 

        # Friction parameters
        self.ticket_fee = SYSTEM_CONFIG["BROKER_COMMISSION_PER_TRADE"]
        self.max_slippage_bps = SYSTEM_CONFIG["MAX_SLIPPAGE_BPS"]

    def _apply_slippage(self, base_price: float, direction: str) -> float:
        """Simulates order book market impact by degrading the execution price."""
        # Convert max basis points to a random float percentage (e.g., 15 bps max = 0.0015 max)
        actual_slippage_pct = random.uniform(0.0, self.max_slippage_bps / 10000.0)
        
        if direction in ["LONG", "EXIT_SHORT"]:
            # Slippage makes buying more expensive
            return round(base_price * (1 + actual_slippage_pct), 2)
        else:
            # Slippage makes selling less profitable
            return round(base_price * (1 - actual_slippage_pct), 2)

    def calculate_allocation(self, signal: dict) -> float:
        asset = signal["asset"]
        direction = signal["direction"]
        raw_price = signal["price"]

        # Deduct transaction fee immediately from the liquid capital pool for any active attempt
        if direction == "EXIT":
            if asset in self.active_positions:
                pos = self.active_positions.pop(asset)
                
                # Apply slippage to the exit execution price
                execution_price = self._apply_slippage(raw_price, "EXIT_LONG" if pos["direction"] == "LONG" else "EXIT_SHORT")
                
                # Calculate absolute return factoring friction
                return_pct = (execution_price / pos["entry_price"]) - 1 if pos["direction"] == "LONG" else 1 - (execution_price / pos["entry_price"])
                gross_pnl = pos["allocated_amount"] * return_pct
                
                # Net PnL = Gross PnL minus the ticket commission fee
                net_pnl = gross_pnl - self.ticket_fee
                
                # Release capital and realize the friction-adjusted net balance return
                self.available_capital += net_pnl
                self.current_allocated_capital -= pos["allocated_amount"]
                
                # Calculate slippage overhead penalty in dollars for reporting metrics
                slippage_penalty = abs(execution_price - raw_price) * (pos["allocated_amount"] / pos["entry_price"])
                
                print(f"[RISK LIQUIDATION] Exited {asset} | Raw: ${raw_price:.2f} -> Executed: ${execution_price:.2f} "
                      f"(Slippage Loss: ${slippage_penalty:.2f}) | Net PnL: ${net_pnl:,.2f}")
            return 0.0

        if asset in self.active_positions:
            return 0.0

        # Core Kelly Sizing Math
        p, b = 0.54, 1.2
        q = 1.0 - p
        raw_kelly = ((b * p) - q) / b
        target_allocation = self.available_capital * (raw_kelly * self.kelly_fraction)
        
        # Enforce exposure safety ceilings
        single_trade_ceiling = self.available_capital * self.max_single_trade_exposure
        if target_allocation > single_trade_ceiling:
            target_allocation = single_trade_ceiling
            
        portfolio_ceiling = SYSTEM_CONFIG["INITIAL_CAPITAL"] * self.max_portfolio_exposure
        if self.current_allocated_capital + target_allocation > portfolio_ceiling:
            target_allocation = portfolio_ceiling - self.current_allocated_capital
            
        # Ensure we have enough dry powder to cover the entry ticket fee
        if target_allocation < 0.01 or self.available_capital < self.ticket_fee:
            return 0.0
            
        return round(target_allocation, 2)

    def update_allocated_risk(self, asset: str, direction: str, raw_price: float, amount: float):
        """Applies entry slippage and logs the trade into the active state register."""
        # Calculate worse entry price via slippage simulation
        execution_price = self._apply_slippage(raw_price, direction)
        
        # Deduct entry ticket commission fee from liquid cash
        self.available_capital -= self.ticket_fee
        self.current_allocated_capital += amount
        
        self.active_positions[asset] = {
            "direction": direction,
            "entry_price": execution_price,
            "allocated_amount": amount
        }
        return execution_price