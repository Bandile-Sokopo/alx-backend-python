# chats/auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication if you want to override behavior later."""
    pass
