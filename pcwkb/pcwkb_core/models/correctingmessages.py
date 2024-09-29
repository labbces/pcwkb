from django.db import models
from django.contrib.auth.models import User

class CorrectionMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="User", null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="Reviewer", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)