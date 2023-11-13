from django.db import models

class PECOTerm(models.Model):
    peco_id = models.CharField(max_length=50, unique=True)
    peco_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.peco_name