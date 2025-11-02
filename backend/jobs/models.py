from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class AsyncJob(models.Model):
    KIND_CHOICES = (("export","export"),)
    STATUS_CHOICES = (("pending","pending"),("running","running"),("done","done"),("error","error"))
    kind = models.CharField(max_length=30, choices=KIND_CHOICES)
    resource = models.CharField(max_length=100)  # ex: pneus.tire
    params = models.JSONField(default=dict, blank=True)
    fmt = models.CharField(max_length=10, default="csv")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    file_path = models.CharField(max_length=300, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-created_at"]
