from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_project, name='add_project'),
    path('edit/<int:id>/', views.edit_project, name='edit_project'),
    path('delete/<int:id>/', views.delete_project, name='delete_project'),
    path('profile/<int:id>/', views.project_profile, name='project_profile'),
    path('hire/<int:user_id>/', views.hire_profile, name='hire_profile'),
    path("hire-now/<int:user_id>/", views.hire_now, name="hire_now"),
    path(
      "hire-inquiry/<int:id>/",
      views.hire_inquiry_detail,
      name="hire_inquiry_detail"
    ),
    path(
        "like/<int:project_id>/",
        views.toggle_like_project,
        name="toggle_like_project"
    ),
    path(
        "appreciate/<int:project_id>/",
        views.toggle_appreciate_project,
        name="toggle_appreciate_project"
    ),
]