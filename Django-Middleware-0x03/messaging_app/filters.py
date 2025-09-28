import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Allows filtering messages by:
    - participant (user id in the conversation)
    - date range (sent_at__gte, sent_at__lte)
    """
    participant = django_filters.NumberFilter(
        field_name="conversation__participants__id", lookup_expr="exact"
    )
    sent_after = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    sent_before = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["participant", "sent_after", "sent_before"]
