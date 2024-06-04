from django.db import models
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript


class CDS(models.Model):
    """Receive cds information
    
    This class stores information about a protein, such as its name, 
    the description of the protein and an ID. 
    """
    cds_name = models.CharField(max_length=100, unique=True)
    cds_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sequence = models.TextField('CDS sequence')
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, null=True, blank=True)
    protein_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.cds_id:
            if self.transcript:  
                self.cds_id = f"{self.transcript.transcript_id}.cds"
            else:
                self.cds_id = f"{self.gene.gene_id}.cds"
        if not self.cds_name:
            if self.transcript:
                self.cds_id = f"{self.transcript.transcript_name}.cds"
            else:
                self.cds_id = f"{self.gene.gene_name}.cds"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cds_name