from django.contrib import admin
from .models import Project, ProjectImage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "visibility", "created_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("title", "user__username")

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "image")
