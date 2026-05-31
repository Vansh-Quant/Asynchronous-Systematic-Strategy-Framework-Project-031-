# alpha_gen.py
"""
Mathematical Signal Generation Engine
Processes streaming tick vectors to calculate directional trading alpha.
"""

from typing import Dict, Optional

class AlphaGenerator:
    def __init__(self):
        # Local window cache to calculate rolling mathematical variance/momentum
        self.window_cache = {}

    def process_tick(self, tick: Dict) -> Optional[Dict]:
        """
        Tracks rolling window ticks.
        Returns a directional signal payload if a clear mathematical edge is found.
        """
        asset = tick["asset"]
        price = tick["price"]
        
        if asset not in self.window_cache:
            self.window_cache[asset] = []
            
        self.window_cache[asset].append(price)
        
        # Enforce memory constraint: track only the last 5 ticks
        if len(self.window_cache[asset]) > 5:
            self.window_cache[asset].pop(0)
            
        # Ensure we have enough data to calculate momentum direction
        if len(self.window_cache[asset]) < 3:
            return None
            
       # Calculate recent vector difference
        prices = self.window_cache[asset]
        immediate_change = prices[-1] - prices[-2]
        prior_change = prices[-2] - prices[-3]
        
        # New upgraded logic: Generate entries AND exits
        if immediate_change > 0 and prior_change > 0:
            return {"asset": asset, "direction": "LONG", "price": price}
        elif immediate_change < 0 and prior_change < 0:
            return {"asset": asset, "direction": "SHORT", "price": price}
        # If price direction stalls or reverses, signal an exit to free up risk capital
        elif (immediate_change < 0 and prior_change > 0) or (immediate_change > 0 and prior_change < 0):
            return {"asset": asset, "direction": "EXIT", "price": price}
            
        return None