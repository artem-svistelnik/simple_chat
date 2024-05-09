from django.contrib.auth.models import User
from django.db import models


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name="participants")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Thread {self.id}"


class Message(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="thread_messages"
    )
    text = models.TextField(max_length=1000)

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender_messages"
    )
    created_at = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message #{self.id}"
