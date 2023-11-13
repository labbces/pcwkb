from django.db import models

class InterPro(models.Model):
    interpro_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)