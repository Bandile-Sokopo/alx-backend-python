from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from chats.models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Create a notification automatically when a new message is received.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            text=f"New message from {instance.sender.username}"
        )

@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def cleanup_user_data(sender, instance, **kwargs):

    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()