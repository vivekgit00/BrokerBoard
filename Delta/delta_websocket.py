import threading
import json
import time
import websocket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
logger = logging.getLogger('custom')


LTP = {}
_ltp_lock = threading.Lock()
class WebSocketManager:
    def __init__(self):
        self.thread = None
        self.ws = None
        self.running = False
        self.symbols = set()
        self.lock = threading.Lock()
        self.connected = threading.Event()
        self.channel = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return False

        print("Starting WebSocket thread...")
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _on_open(self, ws):
        print("WebSocket connected")
        self.connected.set()

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            print("Received:", data)
            if 'symbol' in data and 'price' in data:
                channel_layer = get_channel_layer()

                symbol = data['symbol']
                price = data['price']
                with _ltp_lock:
                    LTP[symbol] = price
                channel_name = self.channel
                if channel_name:
                    channel_layer = get_channel_layer()
                    message = json.dumps(data)
                    async_to_sync(channel_layer.send)(channel_name, {
                        "type": "send_ltp",
                        "text": message
                    })
        except Exception as e:
            print(f"Error processing message: {e}")

    def _on_error(self, ws, error):
        print("WebSocket error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed: {close_status_code}, {close_msg}")
        self.connected.clear()

    def _run(self):
        while self.running:
            self.connected.clear()
            self.ws = websocket.WebSocketApp(
                "wss://socket.india.delta.exchange",
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
            )

            try:
                self.ws.run_forever()
            except Exception as e:
                print(f"WebSocket run_forever exception: {e}")

            print("WebSocket disconnected. Retrying in 5 seconds...")
            time.sleep(5)

    def subscribe(self, new_symbols, channel_name, email):
        # if new_symbols in self.current_symbol:
        #     print(f"Already subscribed to {new_symbols}")
        #     return

        with self.lock:
            self.channel = channel_name
            self.start()
            if not self.connected.wait(timeout=5):
                raise websocket.WebSocketConnectionClosedException("WebSocket not connected")
            print(new_symbols, "444444")
            new_subs = set(new_symbols) - self.symbols
            print(self.symbols, "5555555")
            if not new_subs:
                print("No new symbols to subscribe.")
                return
            payload = {
                "type": "subscribe",
                "payload": {
                    "channels": [{
                        "name": "spot_price",
                        "symbols": list(new_subs)
                    }]
                }
            }

            try:
                self.ws.send(json.dumps(payload))
                self.symbols.update(new_subs)
                print(f"Subscribed to: {new_subs}")
                feed_subscribe_log = False
                if not feed_subscribe_log:

                    print("@@@@@@@@@")
                    feed_subscribe = True
                    logger.info(f"Subscribed to feed{new_subs} email={email}", extra={"email": email})
            except websocket.WebSocketConnectionClosedException:
                print("WebSocket closed during subscribe. Trying to reconnect.")
                self.connected.clear()
    def unsubscribe(self, symbols):
        # if symbols not in self.current_symbol:
        #     return False
        with self.lock:
            to_unsub = set(symbols) & self.symbols
            if not to_unsub:
                print("No symbols to unsubscribe.")
                return
            payload = {
                "type": "unsubscribe",
                "payload": {
                    "channels": [{
                        "name": "spot_price",
                        "symbols": list(to_unsub)
                    }]
                }
            }
            try:
                self.ws.send(json.dumps(payload))
                self.symbols -= to_unsub
                print(f"Unsubscribed from {to_unsub}")
            except websocket.WebSocketConnectionClosedException:
                print("WebSocket closed during unsubscribe.")

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()


# Singleton instance
ws_manager = WebSocketManager()
