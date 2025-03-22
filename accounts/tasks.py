from celery import shared_task
from django.utils import timezone

from .models import OTP


@shared_task
def delete_expired_otps():
    print("inja1")
    print(OTP.objects.all())
    OTP.objects.filter(expires_at__lt=timezone.now()).delete()
