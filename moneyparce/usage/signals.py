from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import LoginEvent

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    LoginEvent.objects.create(user=user, timestamp=now())
