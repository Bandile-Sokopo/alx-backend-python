import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    """
    Middleware to log each request with timestamp, user, and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("request_logs.log")  # log file in project root
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the chat app
    between 6 PM and 9 PM only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allowed hours: 18 (6PM) to 21 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden(
                "Access to the messaging app is restricted outside 6PM–9PM."
            )

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of messages sent per IP.
    Max: 5 POST requests (messages) per 60 seconds.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Track requests per IP: {ip: [timestamps]}
        self.request_log = defaultdict(list)
        self.limit = 5  # max messages
        self.window = 60  # time window in seconds

    def __call__(self, request):
        # Only rate-limit POST requests (message sending)
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self._get_client_ip(request)
            now = time.time()

            # Keep only timestamps within the last window
            self.request_log[ip] = [
                ts for ts in self.request_log[ip] if now - ts < self.window
            ]

            # Check if limit exceeded
            if len(self.request_log[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded: Only 5 messages allowed per minute."
                )

            # Log this request timestamp
            self.request_log[ip].append(now)

        return self.get_response(request)

    def _get_client_ip(self, request):
        """Helper to get client IP from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "")
    
class RolePermissionMiddleware:
    """
    Middleware to restrict access to certain actions based on user role.
    Only 'admin' or 'moderator' roles are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            # Check if request path is for restricted actions
            if request.path.startswith("/api/admin/") or request.path.startswith("/api/moderator/"):
                # User must have role 'admin' or 'moderator'
                user_role = getattr(request.user, "role", None)
                if user_role not in ["admin", "moderator"]:
                    return HttpResponseForbidden("Access denied: Admin or moderator role required.")

        return self.get_response(request)