from django.db import models
from django.contrib.auth.models import User
from pcwkb_core.utils.data_submission import replace_nan_with_none, strip_all_strings
import json

class DataSubmission(models.Model):
    title = models.CharField(max_length=50)
    json_data = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_type = models.CharField(max_length=50)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def clean_json_data(self):
        json_data = json.loads(self.json_data)
        json_data = replace_nan_with_none(json_data)
        json_data = strip_all_strings(json_data)
        self.json_data = json.dumps(json_data)