from django.urls import path
from .views import login_view, profile_view
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('profile/', views.profile_view, name='profile'),
    path('search-users/', views.search_users, name='search_users'),
    path('logout/', LogoutView.as_view(), name='logout'),
]