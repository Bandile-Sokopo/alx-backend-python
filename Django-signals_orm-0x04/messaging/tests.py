from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="12345")
        self.receiver = User.objects.create_user(username="bob", password="12345")

    def test_notification_created_on_message_send(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello, Bob!")
        notification = Notification.objects.filter(user=self.receiver, message=message).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.text, f"New message from {self.sender.username}")
        self.assertFalse(notification.read)