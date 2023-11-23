from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species

class Gene(models.Model):
    """TODO: add comments/ docstrings (try to follow PEP257/ PEP8)"""
    gene_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    original_db = models.CharField(max_length=50, null=True, blank=True)

    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.gene_name
