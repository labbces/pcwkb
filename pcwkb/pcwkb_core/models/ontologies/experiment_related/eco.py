from django.db import models

class ECOTerm(models.Model):
    eco_term = models.CharField(max_length=50, unique=True)
    eco_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.eco_name