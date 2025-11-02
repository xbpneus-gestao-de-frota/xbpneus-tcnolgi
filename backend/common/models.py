from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class AuditLog(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=20)  # create/update/delete
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    details = models.TextField(blank=True)  # JSON dump (request.data)

    class Meta:
        ordering = ["-ts"]
