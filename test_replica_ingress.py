import asyncio
import websockets
import json
from order_book_replica import LocalOrderBookReplica

STREAM_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5@100ms"

async def test_run():
    # Instantiate your replica component
    book = LocalOrderBookReplica(symbol="BTCUSDT")
    print("[SYSTEM] Initializing Local L2 Order Book Replica Core...")
    
    async with websockets.connect(STREAM_URL) as ws:
        print("[NETWORKING] Connected to Live Binance Matching Engine Stream.\n")
        
        frames = 0
        while frames < 20:
            raw_msg = await ws.recv()
            packet = json.loads(raw_msg)
            
            # Feed raw streaming network deltas into your local replica memory maps
            for bid in packet.get('bids', []):
                book.update_level("BUY", float(bid[0]), float(bid[1]))
            for ask in packet.get('asks', []):
                book.update_level("SELL", float(ask[0]), float(ask[1]))
                
            # Simulate routing an institutional order block (3.5 BTC) through your L2 memory
            vwap, slippage = book.calculate_market_impact_fill("BUY", order_size=3.5)
            
            # Print high-fidelity structural execution feedback
            print("\033[H\033[J", end="")
            print("="*80)
            print(f" PORTFOLIO UPGRADE: ANTI-SANDBOX L2 EXECUTION ENGINE [PROJECT #031 CORE]")
            print("="*80)
            print(f"  Asset Context Target : {book.symbol}")
            print(f"  Active Mapped Bids   : {len(book.bids)} price levels in local memory")
            print(f"  Active Mapped Asks   : {len(book.asks)} price levels in local memory")
            print("-"*80)
            print("  INSTITUTIONAL EXECUTION VECTOR SIMULATION (ORDER SIZE: 3.5 BTC):")
            if vwap > 0:
                print(f"    * Simulated Realized VWAP : ${vwap:.2f}")
                print(f"    * Calculated True Slippage: {slippage:.4f} Basis Points (bps)")
            else:
                print("    * Status                  : Bootstrapping Order Book Layers...")
            print("="*80 + "\n")
            
            frames += 1
            await asyncio.sleep(0.001)

if __name__ == "__main__":
    asyncio.run(test_run())