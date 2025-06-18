import websocket
import json

# Delta Exchange production websocket
WEBSOCKET_URL = "wss://socket.india.delta.exchange"

def on_error(ws, error):
    print(f"❌ Socket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"🔌 Socket closed | Code: {close_status_code} | Message: {close_msg}")

def on_open(ws):
    print(f"🔗 Socket connected")

    # Subscribe to spot price of BTC and ETH
    subscribe(ws, "spot_price", [".DEXBTUSD", ".DEXETHUSD"])

def subscribe(ws, channel, symbols):
    payload = {
        "type": "subscribe",
        "payload": {
            "channels": [
                {
                    "name": channel,
                    "symbols": symbols
                }
            ]
        }
    }
    ws.send(json.dumps(payload))
    print(f"📨 Sent subscription for channel '{channel}' with symbols: {symbols}")

def on_message(ws, message):
    message_json = json.loads(message)
    print("📥", message_json)

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
