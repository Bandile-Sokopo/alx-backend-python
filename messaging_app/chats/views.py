from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from chats.permissions import IsParticipantOfConversation
from filters import MessageFilter
from pagination import MessagePagination
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


# -------------------------
# CONVERSATION VIEWSET
# -------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with given participants.
        Expected input:
        {
            "participants": [user_id1, user_id2, ...]
        }
        """
        participants_ids = request.data.get("participants", [])
        if not participants_ids:
            return Response({"error": "At least one participant is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=participants_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        # Only return conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)
    def perform_create(self, serializer):
        # Ensure the creator is added as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


# -------------------------
# MESSAGE VIEWSET
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def create(self, request, *args, **kwargs):
        """
        Send a message in an existing conversation.
        Expected input:
        {
            "conversation": "<conversation_id>",
            "sender": "<user_id>",
            "message_body": "Hello!"
        }
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        body = request.data.get("message_body")

        if not conversation_id or not sender_id or not body:
            return Response({"error": "conversation, sender, and message_body are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        # Ensure sender is part of the conversation
        if sender not in conversation.participants.all():
            return Response({"error": "Sender must be a participant in the conversation"},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        # Show only messages from conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user) 

class IsConversationParticipant(permissions.BasePermission):
    """Only participants can access the conversation"""

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
    
class IsMessageSenderOrRecipient(permissions.BasePermission):
    """Only sender or conversation participants can access the message"""

    def has_object_permission(self, request, view, obj):
        return (
            obj.sender == request.user
            or request.user in obj.conversation.participants.all()
        )
