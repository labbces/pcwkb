from django.db import models
from django.contrib.auth.models import User

class DataSubmission(models.Model):
    title = models.CharField(max_length=50)
    json_data = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_type = models.CharField(max_length=50)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title