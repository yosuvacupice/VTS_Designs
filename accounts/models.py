from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    about_title = models.CharField(max_length=200, blank=True)
    project_description = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username

