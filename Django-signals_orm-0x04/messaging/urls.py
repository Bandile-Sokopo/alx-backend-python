from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from conversations.views import ConversationViewSet
from messages.views import MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename="conversation")
router.register(r'messages', MessageViewSet, basename="message")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
