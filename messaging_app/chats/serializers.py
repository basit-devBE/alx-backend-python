from rest_framework import serializers
from .models import Message
from .models import CustomUser
from .models import Conversation

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'phone_number', 'password_hash', 'role', 'email', 'first_name', 'last_name', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']