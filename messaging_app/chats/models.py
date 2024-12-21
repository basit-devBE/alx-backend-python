from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    # Custom user fields
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password_hash = models.CharField(max_length=128, blank=False, null=False)
    # Role choices
    GUEST = 'guest'
    HOST = 'host'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (GUEST, 'Guest'),
        (HOST, 'Host'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=GUEST)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    # Created timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Indexing
    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants_id = models.ForeignKey(to_field='user_id', to=CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id']),
        ]

    def __str__(self):
        return f'{self.conversation_id}'


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender_id = models.ForeignKey(to_field='user_id', to=CustomUser, on_delete=models.CASCADE)
    message_body = models.TextField(null=False) 
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message_id']),
        ]

    def __str__(self):
        return f'{self.message_id}'  
