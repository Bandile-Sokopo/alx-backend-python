from rest_framework.permissions import BasePermission


class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission:
    - Allow users to access only their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, "sender"):  # If it's a message
            return obj.sender == user
        elif hasattr(obj, "participants"):  # If it's a conversation
            return user in obj.participants.all()
        return False
