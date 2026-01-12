from django.urls import path
from .views import login_view, profile_view
from . import views

urlpatterns = [
    path('', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('search-users/', views.search_users, name='search_users'),
]
