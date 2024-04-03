from django.db import models
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript
from pcwkb_core.models.molecular_components.genetic.proteins import Protein

class CDS(models.Model):
    """Receive cds information
    
    This class stores information about a protein, such as its name, 
    the description of the protein and an ID. 
    """
    cds_name = models.CharField(max_length=100, unique=True)
    cds_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sequence = models.TextField(null=True, blank=True, max_length=20000)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, null=True, blank=True)
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)

    #sequence?
    #FK gene
    #FK transcrito null = true

    def __str__(self):
        return self.cds_name