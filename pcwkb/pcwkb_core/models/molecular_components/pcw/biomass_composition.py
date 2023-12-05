from django.db import models

from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI

class CellWallComponent(models.Model):
    """
    
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    chebi_id = models.ForeignKey(ChEBI, on_delete=models.CASCADE)

    def __str__(self):
        return self.gene_name