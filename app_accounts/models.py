from django.db import models
from app_main.models import BaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .threads import *

class Customers(BaseUser):
    profile_pic = models.ImageField(upload_to="profile", default="profile.jpg", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    online_status = models.BooleanField(default=False)
    def __str__(self):
        return self.email


@receiver(post_save, sender=Customers)
def send_mail(sender,instance,created, **kwargs):
    if created:
        emailID = instance.email
        thread_obj = send_verification_otp(emailID)
        thread_obj.start()