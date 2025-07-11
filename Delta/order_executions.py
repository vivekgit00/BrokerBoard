import requests
import hashlib
import hmac
import requests
import time
import enum
from Delta.delta_websocket import LTP_DATA


class OrderType(enum.Enum):
    LIMIT = "limit_order"
    MARKET = "market_order"

class OrderExecution:
    def __init__(self, order_id, price, quantity, order_type, status):
        self.base_url = 'https://api.india.delta.exchange'
        self.api_key = 'a207900b7693435a8fa9230a38195d'
        self.api_secret = '7b6f39dcf660ec1c7c664f612c60410a2bd0c258416b498bf0311f94228f'
        self.order_type = order_type
        self.order_id = order_id
        self.price = price
        self.quantity = quantity
        self.status = status

    def generate_signature(self, secret, message):
        message = bytes(message, 'utf-8')
        secret = bytes(secret, 'utf-8')
        hash = hmac.new(secret, message, hashlib.sha256)
        return hash.hexdigest()
    def place_order(self):
       pass

    def edit_order(self):
        pass
    def cancel_order(self):
        pass

    def get_order_status(self):
        pass

    def get_order_history(self):
        pass

    def get_open_orders(self):
        pass

    def get_closed_orders(self):
        pass

