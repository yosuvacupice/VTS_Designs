from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    LICENSE_CHOICES = [
        ('all', 'All Rights Reserved'),
        ('free', 'Free to Use'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=200, blank=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    license = models.CharField(max_length=50, choices=LICENSE_CHOICES, default='all')
    allow_download = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="projects/")

class HireInquiry(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_inquiries")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_inquiries")
    hiring_for = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    budget = models.CharField(max_length=50)
    project_description = models.TextField()
    personal_note = models.TextField(blank=True)
    hiring_type = models.CharField(
        max_length=20,
        choices=(("freelancing", "Freelancing"), ("company", "Company"))
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender} → {self.receiver}"