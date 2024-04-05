from django.db import models
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript

class Protein(models.Model):
    """Receive proteins information
    
    This class stores information about a protein, such as its name, 
    the description of the protein and an ID. 
    """
    protein_name = models.CharField(max_length=100, unique=True) #unico | checar se o nome já existe
    protein_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sequence = models.TextField('Protein sequence')
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    transcript= models.ForeignKey(Transcript, on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)

    #sequence?
    #FK transcrito null true
    #FK cds null true
    #FK gene

    def __str__(self):
        return self.protein_name