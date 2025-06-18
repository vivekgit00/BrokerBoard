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
    set_password = models.BooleanField(default=False)
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

class Orders(models.Model):
    user = models.ForeignKey(DeltaBroker, to_field="email", db_column="email", on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.BigIntegerField(null=True, blank=True)
    product_id = models.IntegerField(null=True, blank=True)
    client_order_id = models.CharField(max_length=24, null=True, blank=True)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    side = models.CharField(max_length=10, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    order_type = models.CharField(max_length=50, null=True, blank=True)
    limit_price = models.CharField(max_length=50, null=True, blank=True)

    time_in_force = models.CharField(max_length=50, null=True, blank=True)
    post_only = models.CharField(max_length=50, null=True, blank=True)
    reduce_only = models.CharField(max_length=50, null=True, blank=True)

    order_status = models.CharField(max_length=50, null=True, blank=True)
#     stop_order_type = models.CharField(max_length=50, null=True, blank=True)
#     stop_price = models.CharField(max_length=50, null=True, blank=True)
#
#     trail_amount = models.CharField(max_length=50, null=True, blank=True)
#     stop_trigger_method = models.CharField(max_length=50, null=True, blank=True)
#
#     bracket_stop_trigger_method = models.CharField(max_length=50, null=True, blank=True)
#     bracket_stop_loss_limit_price = models.CharField(max_length=50, null=True, blank=True)
#     bracket_stop_loss_price = models.CharField(max_length=50, null=True, blank=True)
#     bracket_trail_amount = models.CharField(max_length=50, null=True, blank=True)
#     bracket_take_profit_limit_price = models.CharField(max_length=50, null=True, blank=True)
#     bracket_take_profit_price = models.CharField(max_length=50, null=True, blank=True)
#
#     mmp = models.CharField(max_length=50, null=True, blank=True)

#     cancel_orders_accepted = models.CharField(max_length=50, null=True, blank=True)
#
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']






