# alpha_gen.py
"""
Alpha Generation Engine - Threshold Filter Upgrade
Generates directional signals only when momentum exceeds execution friction baselines.
"""

class AlphaGenerator:
    def __init__(self):
        # Independent price history queues for each asset tracking a 5-tick rolling window
        self.price_history = {}
        # MINIMUM PRICE CHANGE REQUIREMENT (Filters out low-alpha slippage traps)
        self.MIN_DELTA_THRESHOLD = {
            "BTC/USD": 12.00,  # Price must move at least $12.00 over 5 ticks to enter
            "ETH/USD": 1.50,   # Price must move at least $1.50 over 5 ticks to enter
            "SOL/USD": 0.15    # Price must move at least $0.15 over 5 ticks to enter
        }

    def process_tick(self, tick: dict) -> dict | None:
        asset = tick["asset"]
        price = tick["price"]

        if asset not in self.price_history:
            self.price_history[asset] = []

        # Maintain a tight rolling lookback horizon
        self.price_history[asset].append(price)
        if len(self.price_history[asset]) > 5:
            self.price_history[asset].pop(0)

        # We need a full history window to reliably calculate velocity thresholds
        if len(self.price_history[asset]) < 5:
            return None

        history = self.price_history[asset]
        
        # Calculate the absolute structural price delta across the lookback horizon
        total_delta = history[-1] - history[0]
        required_threshold = self.MIN_DELTA_THRESHOLD.get(asset, 1.00)

        # Check for active open positions to handle exit conditions cleanly
        # Note: Exits don't use filters; if the trend flips, we get out immediately to protect capital
        is_strictly_increasing = all(x < y for x, y in zip(history, history[1:]))
        is_strictly_decreasing = all(x > y for x, y in zip(history, history[1:]))

        # --- DISCIPLINED MOMENTUM FILTER LOGIC ---
        if is_strictly_increasing and total_delta >= required_threshold:
            return {"asset": asset, "direction": "LONG", "price": price}
            
        elif is_strictly_decreasing and abs(total_delta) >= required_threshold:
            return {"asset": asset, "direction": "SHORT", "price": price}
            
        elif not is_strictly_increasing and not is_strictly_decreasing:
            # If the momentum cascade breaks, fire an exit instantly
            return {"asset": asset, "direction": "EXIT", "price": price}

        return None