# logging_handlers.py
import logging
from django.utils.timezone import now



class LogHandler(logging.Handler):
    def emit(self, record):
        try:
            print(record, "record\n\n")
            email = getattr(record, 'email', None)
            # If user is DeltaBroker instance or attach manually
            from brokers.models import APILog, DeltaBroker

            APILog.objects.create(
                # user=user,
                email=email,
                message=record.getMessage(),
                datetime=now(),
                date=now().date(),
                time=now().time(),
            )
        except Exception as e:
            # Prevent logging errors from crashing your app
            print(f"Logging error: {e}")
