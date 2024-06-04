from django.db import models
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class Transcript(models.Model):
    """Receive transcripts information
    
    This class stores a transcript sequence and requires a related genes 
    that needs to be in our database.
    """
    transcript_name = models.CharField(max_length=100, unique=True)
    transcript_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sequence = models.TextField('Trancript sequence')
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE) #FK gene
    source = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.transcript_id:
            self.transcript_id = f"{self.gene.gene_id}.t"
        if not self.transcript_name:
            self.transcript_id = f"{self.gene.gene_name}.t"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.transcript_name