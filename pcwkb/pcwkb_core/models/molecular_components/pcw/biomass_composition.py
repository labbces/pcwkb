from django.db import models

from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI

class CellWallComponent(models.Model):
    """Receive plant cell wall information
    
    This class stores information about plant cell wall composition, such as its name, 
    the description of the composition and the ChEBI ID for the components, stored in ChEBI class.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    chebi_id = models.ForeignKey(ChEBI, on_delete=models.CASCADE)

    def __str__(self):
        return self.gene_name