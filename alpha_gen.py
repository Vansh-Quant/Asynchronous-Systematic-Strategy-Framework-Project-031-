# alpha_gen.py
"""
Alpha Generation Engine - Volatility-Filtered Dual Moving Average Cross Loop
Integrates ATR filtering and a state tracker to stop duplicate signal spamming.
"""

class AlphaGenerator:
    def __init__(self):
        self.price_history = {}
        
        # Internal state tracker to remember active trade states per asset
        self.current_positions = {
            "BTC/USD": "NONE",
            "ETH/USD": "NONE",
            "SOL/USD": "NONE"
        }
        
        self.FAST_WINDOW = 10   
        self.SLOW_WINDOW = 30   
        self.ATR_WINDOW = 14    
        
        self.ATR_THRESHOLD = {
            "BTC/USD": 45.00,   
            "ETH/USD": 4.50,    
            "SOL/USD": 0.35     
        }

    def _calculate_atr(self, history: list) -> float:
        if len(history) < self.ATR_WINDOW + 1:
            return 0.0
        true_ranges = []
        for i in range(1, len(history)):
            tr = abs(history[i] - history[i-1])
            true_ranges.append(tr)
        target_window = true_ranges[-self.ATR_WINDOW:]
        return sum(target_window) / self.ATR_WINDOW

    def process_tick(self, tick: dict) -> dict | None:
        asset = tick["asset"]
        price = tick["price"]

        if asset not in self.price_history:
            self.price_history[asset] = []

        self.price_history[asset].append(price)
        
        max_buffer = self.SLOW_WINDOW + 5
        if len(self.price_history[asset]) > max_buffer:
            self.price_history[asset].pop(0)

        if len(self.price_history[asset]) < self.SLOW_WINDOW:
            return None

        history = self.price_history[asset]

        # --- VOLATILITY REGIME GATE ---
        current_atr = self._calculate_atr(history)
        min_allowed_volatility = self.ATR_THRESHOLD.get(asset, 1.00)
        
        if current_atr < min_allowed_volatility:
            return None 

        # --- COMPUTE VECTORIZED MOVING AVERAGES ---
        fast_ma = sum(history[-self.FAST_WINDOW:]) / self.FAST_WINDOW
        slow_ma = sum(history[-self.SLOW_WINDOW:]) / self.SLOW_WINDOW

        # --- STATE-AWARE EXECUTION MACHINE ---
        if fast_ma > slow_ma:
            if self.current_positions[asset] != "LONG":
                self.current_positions[asset] = "LONG"
                return {"asset": asset, "direction": "LONG", "price": price}
            return None 

        elif fast_ma < slow_ma:
            if self.current_positions[asset] != "SHORT":
                self.current_positions[asset] = "SHORT"
                return {"asset": asset, "direction": "SHORT", "price": price}
            return None 
            
        else:
            if self.current_positions[asset] != "NONE":
                self.current_positions[asset] = "NONE"
                return {"asset": asset, "direction": "EXIT", "price": price}
            return None