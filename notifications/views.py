from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications
    })

@login_required
def mark_notification_read(request, id):
    note = get_object_or_404(Notification, id=id, user=request.user)
    note.is_read = True
    note.save()
    return render(request, "notifications/notification_read.html", {
        "notification": note
    })


