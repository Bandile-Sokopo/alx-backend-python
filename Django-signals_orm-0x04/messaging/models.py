from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q, Count
from django.utils import timezone

# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """String representation with participant emails."""
        participants = ', '.join(self.participants.values_list('email', flat=True)[:3])  # Limit for performance
        return f"Conversation {self.conversation_id} ({participants})"

    @classmethod
    def get_or_create_conversation(cls, participant_ids):
        """
        Get or create a conversation for a set of participants.
        """
        conversations = cls.objects.filter(participants__in=participant_ids).annotate(
            num_participants=Count('participants')
        ).filter(num_participants=len(participant_ids))
        for conv in conversations:
            if set(conv.participants.values_list('user_id', flat=True)) == set(participant_ids):
                return conv
        conv = cls.objects.create()
        conv.participants.add(*User.objects.filter(user_id__in=participant_ids))
        return conv

    class Meta:
        indexes = [models.Index(fields=['participants'])]

# Message Model
class Message(models.Model):
    class Status(models.TextChoices):
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        READ = 'read', 'Read'

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    message_body = models.TextField(max_length=10000)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SENT)
    deleted_at = models.DateTimeField(null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    objects = models.Manager()
    unread = UnreadMessagesManager() 

    def __str__(self):
        """Optimized string representation."""
        return f"Message {self.message_id} by {self.sender_id} in {self.conversation_id}"

    class Meta:
        ordering = ['sent_at']
        indexes = [models.Index(fields=['conversation', 'sent_at'])]


    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.text}"
    
@method_decorator(cache_page(60), name='dispatch')
class MessageHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for a specific user.
        Optimized with `.only()` to load only required fields.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")  # optimize foreign key lookups
        )