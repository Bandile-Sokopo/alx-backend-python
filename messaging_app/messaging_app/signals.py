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


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving a Message update, store the old content into MessageHistory.
    - Trigger only on updates (not create).
    - Create a MessageHistory object using MessageHistory.objects.create(...)
    - Mark instance.edited = True and preserve edited_by if provided (e.g., set by view)
    """
    if instance._state.adding:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content != instance.content:
        edited_by_user = getattr(instance, "edited_by", None)

        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            edited_at=timezone.now(),
            edited_by=edited_by_user,
        )

        # mark this message as edited
        instance.edited = True