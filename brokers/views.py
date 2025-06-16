from .models import DeltaBroker
from rest_framework import viewsets
from .serializer import DeltaBrokerSerializer
from rest_framework.decorators import action
from brokers.utils import custom_response, email_password, send_otp_email
from django.utils.crypto import get_random_string
import  random, string
import logging
# from .delta_client import active_symbols, client_symbol_map
from Delta.websocket import subscribe_symbols
import threading
from .serializer import OrdersSerializer
from .models import Orders

logger = logging.getLogger('custom')



class DeltaBrokerView(viewsets.ModelViewSet):
    queryset = DeltaBroker.objects.all()
    serializer_class = DeltaBrokerSerializer

    @action(methods=['post'], detail=False, url_path='select_broker')
    def select_broker(self, request):
        data = request.data
        email = request.data.get('email')
        phone = request.data.get('phone_number')
        logger.info(f"Broker selection attempt: email={email}",extra={'email': email})
        client_id = request.data.get('client_id')
        if DeltaBroker.objects.filter(email=email).exists() and DeltaBroker.objects.filter(phone_number=phone).exists():
            logger.error(f"Email or phone number already exists email={email} ", extra={'email': email})
            return custom_response(message="email or phone_number already exists", status=0)
        if DeltaBroker.objects.filter(client_id=client_id).exists():
            return custom_response(message="client_id already exists", status=0)

        generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        print(generated_password)

        serializer = DeltaBrokerSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(password=generated_password)
            email_password(data.get("broker"), generated_password, email)
            logger.info(f"New broker registered: email={email}, client_id={client_id}", extra={'request': request})
            return  custom_response(message="ok", status=1, data=serializer.data)
        return custom_response(message="not_ok", status=0, data=serializer.errors)

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        logger.info(f"Login attempt: email={email}", extra={'email': email})
        if not DeltaBroker.objects.filter(email=email).exists():
            return custom_response(message="email not exists", status=0)
        if not DeltaBroker.objects.filter(password=password).exists():
            return custom_response(message="password not exists", status=0)
        serializer = DeltaBrokerSerializer(DeltaBroker.objects.get(email=email))
        logger.info(f"Login attempt Successful: email={email}", extra={'email': email})
        return custom_response(message="Login Successful", status=1)

    @action(methods=['post'], detail=False, url_path='change_password')
    def change_password(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        logger.info(f"Password Change Attempt: email={email}", extra={'email': email})
        if not DeltaBroker.objects.filter(email=email).exists():
            logger.error(f"email not exists: email={email}", extra={'email': email})
            return custom_response(message="email not exists", status=0)
        if not DeltaBroker.objects.filter(password=password).exists():
            logger.error(f"password not match: email={email}", extra={'email': email}  )
            return custom_response(message="password not exists", status=0)
        DeltaBroker.objects.filter(email=email).update(password=new_password)
        logger.info(f"Password Changed Successfully: email={email}", extra={'email': email})
        return custom_response(message="Password Changed Successfully", status=1)

    @action(methods=['post'], detail=False, url_path='otp_verify')  # For Account Update Verification
    def otp_verify(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        logger.info(f"OTP Verification Attempt: email={email}", extra={'email': email})
        if not DeltaBroker.objects.filter(email=email).exists():
            return custom_response(message="email not exists", status=0)
        if not DeltaBroker.objects.filter(otp_code=otp).exists():
            logger.error("Incorrect OTP", extra={'email': email})
            return custom_response(message="Incorrect OTP", status=0)
        DeltaBroker.objects.filter(email=email).update(otp_verified=True)
        logger.info(f"OTP Verified Successfully: email={email}", extra={'email': email})
        return custom_response(message="OTP Verified Successfully", status=1)

    @action(methods=['post'], detail=False, url_path='send_otp')
    def send_otp_email(self, request):
        email = request.data.get('email')
        logger.info(f"OTP Sent Attempt: email={email}", extra={'email': email})
        if not DeltaBroker.objects.filter(email=email).exists():
            return custom_response(message="email not exists", status=0)
        otp = get_random_string(length=6, allowed_chars='0123456789')
        print("email otp account update --->>>>>", otp)
        send_otp_email(email, otp)
        logger.info(f"OTP Sent Successfully: email={email}", extra={'email': email})
        DeltaBroker.objects.filter(email=email).update(otp_code=otp)
        return custom_response(message="OTP Sent Successfully", status=1)

    @action(methods=['post'], detail=False, url_path='update_profile')
    def update_profile(self, request):
        email = request.data.get('email')
        print(DeltaBroker.otp_verified)
        logger.info(f"Profile Update Attempt: email={email}", extra={'email': email})
        if DeltaBroker.otp_verified:
            if not DeltaBroker.objects.filter(email=email).exists():
                return custom_response(message="email not exists", status=0)
            serializer = DeltaBrokerSerializer(DeltaBroker.objects.get(email=email), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profile Updated Successfully: email={email}", extra={'email': email})
                return custom_response(message="Profile Updated Successfully", status=1, data=serializer.data)
            return custom_response(message="Profile Not Updated", status=0)
        else:
            logger.error("OTP Not Verified", extra={'email': email})
            return custom_response(message="OTP Not Verified", status=0)

    @action(methods=['delete'], detail=False, url_path='delete_profile')
    def delete_profile(self, request):
        email = request.data.get('email')
        logger.info(f"Profile Delete Attempt: email={email}", extra={'email': email})
        if not DeltaBroker.objects.filter(email=email).exists():
            return custom_response(message="email not exists", status=0)
        DeltaBroker.objects.filter(email=email).delete()
        logger.info(f"Profile Deleted Successfully: email={email}", extra={'email': email})
        return custom_response(message="Profile Deleted Successfully", status=1)
    
    @action(methods=['get'], detail=False, url_path='get_profile')
    def get_profile(self, request):
        email = request.query_params.get('email')
        logger.info(f"Profile Get Attempt: email={email}", extra={'email': email})
        if not DeltaBroker.objects.filter(email=email).exists():
            return custom_response(message="email not exists", status=0)
        serializer = DeltaBrokerSerializer(DeltaBroker.objects.get(email=email))
        logger.info(f"Profile Get Successfully: email={email}", extra={'email': email})
        return custom_response(message="Profile Get Successfully", status=1, data=serializer.data)

class DeltaWebsocket(viewsets.ViewSet):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.symbols = []
    #     with open('delta_symbols.json', 'r') as f:
    #         self.symbols =json.load(f)

    @action(methods=['post'], detail=False, url_path='live_feed')
    def live_feed(self, request):
        symbols = request.data.get("symbols")  # e.g., ["BTCUSD", "ETHUSD"]
        channel_name = request.data.get("channel")  # frontend's WebSocket channel name
        request_type = request.data.get("request_type")
        print(request_type)
        if not symbols or not channel_name:
            return custom_response(message="Missing symbols or channel name", status=0)

        thread = False
        # Launch Delta socket in background
        thread = threading.Thread(target=subscribe_symbols, args=(symbols, channel_name, request_type))
        thread.start()
        
        return custom_response(message=f"{request_type} request sent", status=1)

class ordersView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

