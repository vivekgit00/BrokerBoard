import websocket
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

active_symbol = {}

def subscribe_symbols(symbols, channel_name, request_type):
    ws = None
    global active_symbol
    def on_message(ws_inner, message):
        data = json.loads(message)
        print("Received from Delta:", data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(channel_name, {
            "type": "send_ltp",
            "text": json.dumps(data)
        })

    def on_error(ws_inner, error):
        print(f"Socket Error: {error}")

    def unsubscribe_symbols(ws_inner, channel, symbols):
        print("unsubscribe")
        payload = {
            "type": "unsubscribe",
            "payload": {
                "channels": [
                    {
                        "name": channel,
                        "symbols": symbols
                    }
                ]
            }
        }
        print("Unsubscribe Payload:", payload)
        ws_inner.send(json.dumps(payload))
        if channel_name in active_symbol:
            active_symbol[channel_name] -= set(symbols)
            if not active_symbol[channel_name]:
                del active_symbol[channel_name]

    def subscribe_symbols(ws_inner, channel, symbols):
        print("subscribe")
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
        ws_inner.send(json.dumps(payload))
        active_symbol[channel_name] = set(symbols)

    def on_open(ws_inner):
        print("Connected to Delta")
        if request_type == "subscribe":
            subscribe_symbols(ws_inner, "candlestick_1m", symbols)
        elif request_type == "unsubscribe":
            unsubscribe_symbols(ws_inner, "candlestick_1m", symbols)

    ws = websocket.WebSocketApp(
        "wss://socket.india.delta.exchange",
        on_open=on_open,
        on_error=on_error,
        on_message=on_message,
    )

    ws.run_forever()