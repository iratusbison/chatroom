from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    username = models.CharField(max_length=255, null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.message} ({self.timestamp})"
