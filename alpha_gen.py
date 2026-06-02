# alpha_gen.py
"""
Alpha Generation Engine - Dual Moving Average Cross Loop
Utilizes vectorized lookbacks to isolate macro trends and reject micro-noise.
"""

class AlphaGenerator:
    def __init__(self):
        # Rolling price cache for multi-asset processing
        self.price_history = {}
        # Dynamic lookback parameters
        self.FAST_WINDOW = 5
        self.SLOW_WINDOW = 15
        
        # Absolute price velocity thresholds required to justify execution friction
        self.MIN_VELOCITY_THRESHOLD = {
            "BTC/USD": 8.00,
            "ETH/USD": 1.00,
            "SOL/USD": 0.10
        }

    def process_tick(self, tick: dict) -> dict | None:
        asset = tick["asset"]
        price = tick["price"]

        if asset not in self.price_history:
            self.price_history[asset] = []

        self.price_history[asset].append(price)
        
        # Keep window bounded cleanly to the max required slow lookback size
        if len(self.price_history[asset]) > self.SLOW_WINDOW:
            self.price_history[asset].pop(0)

        # Restrict execution initialization until the slow window is completely saturated
        if len(self.price_history[asset]) < self.SLOW_WINDOW:
            return None

        history = self.price_history[asset]

        # --- COMPUTE VECTORIZED MOVING AVERAGES ---
        fast_ma = sum(history[-self.FAST_WINDOW:]) / self.FAST_WINDOW
        slow_ma = sum(history[-self.SLOW_WINDOW:]) / self.SLOW_WINDOW
        
        # Calculate trailing momentum momentum velocity
        recent_velocity = history[-1] - history[-3]
        required_threshold = self.MIN_VELOCITY_THRESHOLD.get(asset, 0.50)

        # --- EXECUTION STATE MACHINE ---
        # Signal LONG if fast momentum crosses above slow baseline AND velocity breaks out
        if fast_ma > slow_ma and recent_velocity >= required_threshold:
            return {"asset": asset, "direction": "LONG", "price": price}
            
        # Signal SHORT if fast momentum breaks below slow baseline AND velocity breaks out downward
        elif fast_ma < slow_ma and recent_velocity <= -required_threshold:
            return {"asset": asset, "direction": "SHORT", "price": price}
            
        # Clear out positions immediately if moving averages converge (loss of momentum edge)
        else:
            return {"asset": asset, "direction": "EXIT", "price": price}