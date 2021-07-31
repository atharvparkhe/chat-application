from django.db import models

class ChatManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class RoomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)