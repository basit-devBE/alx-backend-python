from rest_framework import serializers
from .models import CustomUser,Conversation,Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['user_id', 'full_name', 'phone_number', 'role', 'email', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    formatted_sent_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'formatted_sent_at']
        read_only_fields = ['message_id', 'sent_at']

        def get_formatted_sent_at(self, obj):
            return obj.sent_at.strftime('%b %d %Y %I:%M %p')
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True
    )
    initial_messages = MessageSerializer(write_only=True, required=False)
    class Meta:
        model = Conversation
        fields = ['participants', 'conversation_id', 'created_at', 'initial_messages']