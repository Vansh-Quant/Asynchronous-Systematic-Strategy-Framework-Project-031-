import asyncio
import websockets
import json
import logging
from order_book_replica import LocalOrderBookReplica

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [INGRESS] - %(message)s')

class LiveDataIngress:
    def __init__(self, symbol: str = "BTCUSDT"):
        self.symbol = symbol.lower()
        self.stream_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@depth5@100ms"
        self.order_book = LocalOrderBookReplica(symbol=symbol.upper())
        self.is_running = False

    async def start_stream(self, queue: asyncio.Queue):
        """Maintains connection to exchange feed and pushes updated book snapshots to the engine queue."""
        self.is_running = True
        logging.info(f"Initializing live stream channel for {self.symbol.upper()}...")

        while self.is_running:
            try:
                async with websockets.connect(self.stream_url, open_timeout=15) as ws:
                    logging.info("WebSocket handshake verified. Streaming market depth updates.")
                    
                    while self.is_running:
                        raw_msg = await ws.recv()
                        packet = json.loads(raw_msg)
                        
                        # Apply raw network deltas to the local memory layer
                        for bid in packet.get('bids', []):
                            self.order_book.update_level("BUY", float(bid[0]), float(bid[1]))
                        for ask in packet.get('asks', []):
                            self.order_book.update_level("SELL", float(ask[0]), float(ask[1]))

                        # Calculate current mid-price to serve as baseline framework context
                        if book_asks := self.order_book.asks:
                            if book_bids := self.order_book.bids:
                                mid_price = (min(book_asks.keys()) + max(book_bids.keys())) / 2.0
                                
                                # Send current book snapshot reference up to the master coordinator loop
                                payload = {
                                    "mid_price": mid_price,
                                    "book_ref": self.order_book
                                }
                                await queue.put(payload)
                                
                        await asyncio.sleep(0.001)

            except (websockets.exceptions.ConnectionClosed, asyncio.TimeoutError) as e:
                logging.warning(f"Network disconnection detected: {e}. Reconnecting in 3 seconds...")
                await asyncio.sleep(3)
            except Exception as e:
                logging.error(f"Critical execution fault in data ingress stream: {e}")
                self.is_running = False