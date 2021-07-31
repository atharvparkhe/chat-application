from django.db import models
from app_main.models import BaseModel
from app_accounts.models import Customers
from .manager import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Room(BaseModel):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="room", null=True, blank=True)
    members = models.ManyToManyField(Customers)
    is_deleted = models.BooleanField(default=False)
    objects = RoomManager()
    admin_objects = models.Manager()

@receiver(pre_save, sender=Room)
def generate_slug(sender,instance, **kwargs):
    instance.name = slugify(instance.name)

class Chat(BaseModel):
    group = models.ForeignKey(Room, related_name="group", on_delete=models.CASCADE)
    sender = models.ForeignKey(Customers, related_name="sender", on_delete=models.PROTECT)
    message = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    objects = ChatManager()
    admin_objects = models.Manager()