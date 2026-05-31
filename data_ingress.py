# data_ingress.py
"""
Asynchronous Data Ingress Engine
Simulates live, non-blocking market data feeds for specified multi-asset universes.
"""

import asyncio
import random
import time
from typing import AsyncGenerator, Dict
from config import SYSTEM_CONFIG

class AsynchronousIngress:
    def __init__(self):
        self.assets = SYSTEM_CONFIG["ASSET_UNIVERSE"]
        # Initialize seed prices for simulation
        self.price_matrix = {"BTC/USD": 65000.0, "ETH/USD": 3400.0, "SOL/USD": 140.0}
        self.delay = SYSTEM_CONFIG["DATA_STREAM_DELAY"]

    async def stream_ticks(self) -> AsyncGenerator[Dict, None]:
        """
        Asynchronously generates continuous, non-blocking asset price ticks.
        Yields a normalized payload vector: {timestamp, asset, price}
        """
        while True:
            # Pick a random asset to generate a tick for
            asset = random.choice(self.assets)
            base_price = self.price_matrix[asset]
            
            # Simulate a small random percentage price shock (-0.2% to +0.2%)
            shock = random.uniform(-0.002, 0.002)
            new_price = round(base_price * (1 + shock), 2)
            
            # Update internal state matrix
            self.price_matrix[asset] = new_price
            
            # Pack the normalized data payload vector
            payload = {
                "timestamp": time.time(),
                "asset": asset,
                "price": new_price
            }
            
            yield payload
            
            # Non-blocking pause to allow the event loop to switch contexts
            await asyncio.sleep(self.delay)