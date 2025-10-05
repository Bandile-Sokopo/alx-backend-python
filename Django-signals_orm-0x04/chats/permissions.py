from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission:
    - Authenticated users only
    - Participants can view conversations/messages
    - Only owners (senders) can update or delete their messages
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # READ-ONLY access (GET, HEAD, OPTIONS) -> allowed for participants
        if request.method in SAFE_METHODS:
            if hasattr(obj, "participants"):  # Conversation
                return user in obj.participants.all()
            if hasattr(obj, "sender"):  # Message
                return obj.conversation.participants.filter(id=user.id).exists()

        # WRITE access (PUT, PATCH, DELETE) -> only the sender can edit/delete their own message
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, "sender"):  # For messages
                return obj.sender == user
            if hasattr(obj, "participants"):  # For conversation
                # Optional: only allow conversation creator/admin to edit
                return obj.created_by == user if hasattr(obj, "created_by") else False

        # Default deny
        return False
