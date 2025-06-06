from django.utils.crypto import get_random_string
otp = get_random_string(length=6, allowed_chars='0123456789')
print(otp)