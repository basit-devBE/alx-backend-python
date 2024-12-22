from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationCreateSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationCreateSerializer

    def get_queryset(self):
        # Filter conversations where the logged-in user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['request'] = request  # Pass the request context for the sender
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            {"message": "Conversation created successfully!", "conversation": serializer.data},
            status=status.HTTP_201_CREATED
        )

from rest_framework.decorators import action

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Filter messages for a specific conversation
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return self.queryset.filter(conversation_id=conversation_id)
        return self.queryset.none()

    @action(detail=False, methods=['post'], url_path='send')
    def send_message(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response(
                {"error": "Both conversation_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                message_body=message_body
            )
            return Response(
                {"message": "Message sent successfully!", "message_data": MessageSerializer(message).data},
                status=status.HTTP_201_CREATED
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
