from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users
    who are participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users to access the API at all
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Checks if the authenticated user is part of the conversation.
        Works for Conversation and Message objects.
        """
        if hasattr(obj, "participants"):  # Conversation instance
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # Message instance
            return request.user in obj.conversation.participants.all()

        return False
