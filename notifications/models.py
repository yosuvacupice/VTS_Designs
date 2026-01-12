from django.db import models
from django.contrib.auth.models import User
from projects.models import HireInquiry

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
        null=True,
        blank=True
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    hire_inquiry = models.ForeignKey(
        HireInquiry,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.text
