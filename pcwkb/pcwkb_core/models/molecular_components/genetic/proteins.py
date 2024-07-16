from django.db import models
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript
from pcwkb_core.models.molecular_components.genetic.cds import CDS


class Protein(models.Model):
    """Receive proteins information
    
    This class stores information about a protein, such as its name, 
    the description of the protein and an ID. 
    """
    protein_id = models.CharField(max_length=100, unique=True, null=True, blank=True) #protein identifier unique
    protein_name = models.CharField(max_length=100, null=True, blank=True) #protein name
    description = models.TextField(null=True, blank=True) #protein description
    sequence = models.TextField('Protein sequence') #protein sequence
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    transcript= models.ForeignKey(Transcript, on_delete=models.CASCADE, null=True, blank=True)
    cds = models.ForeignKey(CDS, on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.protein_id:
            if self.transcript:  
                self.protein_id = f"{self.transcript.transcript_id}.p"
            else:
                self.protein_id = f"{self.gene.gene_id}.p"
        if not self.protein_name:
            if self.transcript:
                self.protein_name = f"{self.transcript.transcript_name}.p"
            else:
                self.protein_name = f"{self.gene.gene_name}.p"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.protein_name