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


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Allow the authenticated user to delete their account.
    This triggers automatic cleanup of related data via signals.
    """
    user = request.user
    username = user.username
    user.delete()
    return Response({"message": f"User '{username}' and related data deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_messages_view(request):
    """
    Return all unread messages for the authenticated user.
    Uses custom manager for efficiency.
    """
    user = request.user
    unread_messages = Message.unread.for_user(user)
    serializer = MessageSerializer(unread_messages, many=True)
    return Response(serializer.data)