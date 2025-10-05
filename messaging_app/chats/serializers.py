from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------
# USER SERIALIZER
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]


# -------------------------
# MESSAGE SERIALIZER
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "__all__"
        ]
        read_only_fields = ["message_id", "sent_at"]

    def get_replies(self, obj):
        replies = obj.replies.all()
        return MessageSerializer(replies, many=True).data


# -------------------------
# CONVERSATION SERIALIZER
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "__all__"
        ]
        read_only_fields = ["conversation_id", "created_at"]
