from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications'),
    path('read/<int:id>/', views.mark_notification_read, name='notification_read'),
]
