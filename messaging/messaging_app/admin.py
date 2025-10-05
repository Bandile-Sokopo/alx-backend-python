from django.contrib import admin
from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "timestamp", "content")
    list_filter = ("sender", "receiver", "timestamp")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "text", "created_at", "read")
    list_filter = ("user", "read", "created_at")