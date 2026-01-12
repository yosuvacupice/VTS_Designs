from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Project
from chat.models import Message
from notifications.models import Notification
from django.contrib.auth.models import User

@login_required
def dashboard_view(request):
    user = request.user
    total_projects = Project.objects.filter(user=user).count()
    total_messages = Message.objects.filter(receiver=user).count()
    recent_messages = Message.objects.filter(receiver=user).order_by('-created_at')[:2]
    total_notifications = Notification.objects.filter(user=user).count()
    recent_notifications = Notification.objects.filter(user=user).order_by('-created_at')[:2]
    total_candidates = User.objects.exclude(id=user.id).count()
    available_candidates = User.objects.exclude(id=user.id)[:2]
    context = {
        'total_projects': total_projects,
        'total_messages': total_messages,
        'total_candidates': total_candidates,
        'total_notifications': total_notifications,
        'recent_messages': recent_messages,
        'recent_notifications': recent_notifications,
        'available_candidates': available_candidates, 
    }
    return render(request, 'dashboard/dashboard.html', context)