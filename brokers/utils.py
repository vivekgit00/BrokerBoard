from rest_framework.response import Response
from django.core.mail import send_mail
import random
def custom_response(message="OK", status=1, data=""):
    return Response({
        "message": message,
        "status": status,
        "data": data
    })

def email_password(broker, generated_password, email):
     send_mail(
            subject='Temporary auto-generated password',
            message=f'Your temporary password for login to {broker} website is: {generated_password}\n'
                    f'Make sure to change the password after first login.',
            from_email="kunals4a@gmail.com",
            recipient_list=[email],
            fail_silently=False,
            )
def generate_otp():
    return str(random.randint(100000, 999999))
def send_otp_email(email, otp):
    send_mail(
        subject='*BrokerBoard* Your DeltaBroker Account Update Verification OTP ',
        message=f'Your OTP code is {otp}',
        from_email="kunals4a@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )