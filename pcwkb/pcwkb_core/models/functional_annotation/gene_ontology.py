from django.db import models
from pcwkb_core.models.molecular_components.genes import Gene

class GeneOntologyTerm(models.Model):
    go_id = models.CharField(max_length=50, unique=True)
    go_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    gene_id = models.ForeignKey(Gene, on_delete=models.CASCADE)

    def __str__(self):
        return self.go_name
