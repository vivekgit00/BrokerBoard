import websocket
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def subscribe_symbols(symbols, channel_name, request_type):
    ws = None

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

    def subscribe_symbols(ws_inner, channel, symbols):
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