from django.db import models
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class Transcript(models.Model):
    """Receive transcripts information
    
    This class stores a transcript sequence and requires a related genes 
    that needs to be in our database.
    """
    sequence = models.TextField('Trancript sequence', max_length=12000)

    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

    def __str__(self):
        return self.sequence