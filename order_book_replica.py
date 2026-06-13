import math

class LocalOrderBookReplica:
    """
    Tracks full local L2 market depth state from streaming delta updates.
    Eliminates basic sandbox price assumptions by enforcing real-market execution physics.
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Python dicts preserve insertion order; we sort them when running execution passes
        self.bids = {}  # { price_float: qty_float }
        self.asks = {}  # { price_float: qty_float }

    def update_level(self, side: str, price: float, quantity: float):
        """Processes live delta packets, handling volume shifts and depth structural erasures."""
        if side.upper() == "BUY":
            if quantity == 0.0:
                self.bids.pop(price, None)  # Liquidity layer fully depleted or canceled
            else:
                self.bids[price] = quantity  # Insert or overwrite price layer volume
        elif side.upper() == "SELL":
            if quantity == 0.0:
                self.asks.pop(price, None)
            else:
                self.asks[price] = quantity

    def calculate_market_impact_fill(self, action: str, order_size: float):
        """
        Anti-Sandbox Logic: Sweeps through real available depth rows sequentially.
        Calculates the exact non-linear realized VWAP and true microstructural slippage.
        """
        if action.upper() == "BUY":
            if not self.asks: return 0.0, 0.0
            # Sort asks ascending: lowest sellers at the top of the book (L1 Best Ask)
            sorted_layers = sorted(self.asks.items(), key=lambda x: x[0])
        else:
            if not self.bids: return 0.0, 0.0
            # Sort bids descending: highest buyers at the top of the book (L1 Best Bid)
            sorted_layers = sorted(self.bids.items(), key=lambda x: x[0], reverse=True)

        remaining_qty = order_size
        total_notional_cost = 0.0
        baseline_price = sorted_layers[0][0]  # The initial quote price at L1

        for price, qty in sorted_layers:
            match_qty = min(remaining_qty, qty)
            total_notional_cost += (match_qty * price)
            remaining_qty -= match_qty
            
            if remaining_qty <= 0.0:
                break

        # If the requested order size sweeps past our entire order book depth,
        # fill the remaining units at the final boundary tier price
        if remaining_qty > 0.0:
            total_notional_cost += (remaining_qty * price)

        realized_vwap = total_notional_cost / order_size
        # Slippage calculation converted to precise institutional Basis Points (1 bps = 0.01%)
        slippage_bps = (abs(realized_vwap - baseline_price) / baseline_price) * 10000.0

        return realized_vwap, slippage_bps

    def clear_book(self):
        """Resets book states cleanly during system desynchronization events."""
        self.bids.clear()
        self.asks.clear()