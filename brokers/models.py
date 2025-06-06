from django.db import models
from django.utils.timezone import  now
# Create your models here.
class DeltaBroker(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    client_id = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=100, null=True, blank=True)
    api_secret = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=16, null=True, blank=True)
    broker_name = models.CharField(max_length=50, null=True, blank=True)

    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'delta_users'
        ordering = ['-created_at']


class APILog(models.Model):
    email = models.EmailField(null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)

    datetime = models.DateTimeField(default=now)
    date = models.DateField(default=now)
    time = models.TimeField(default=now)


    def __str__(self):
        return f"Log by {self.email or 'Anonymous'} at {self.datetime}"

    class Meta:
        db_table = 'api_logs'
        ordering = ['-datetime']