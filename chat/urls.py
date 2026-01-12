from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages_view, name='messages'),
    path('compose/', views.compose_message, name='compose_message'),
    path('search-users/', views.search_users, name='search_users'),
    path('<int:id>/', views.message_detail, name='message_detail'),
]
