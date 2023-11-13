from django.db import models

class Protein(models.Model):
    protein_id = models.CharField(max_length=50, unique=True)
    protein_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.protein_name