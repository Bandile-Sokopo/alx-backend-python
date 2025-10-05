from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages.
    - 20 messages per page by default
    - Clients can override with ?page_size=50 (max 100)
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
