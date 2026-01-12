from chat.models import Message
from notifications.models import Notification

def header_counts(request):
    if request.user.is_authenticated:
        unread_messages = Message.objects.filter(
            receiver=request.user
        ).count()
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
    else:
        unread_messages = 0
        unread_notifications = 0
    return {
        "unread_messages": unread_messages,
        "unread_notifications": unread_notifications
    }


from .models import Notification
def notification_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications': Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
        }
    return {'unread_notifications': 0}
