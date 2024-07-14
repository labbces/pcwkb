from django.db import models

class PECOTerm(models.Model):
    """Receive PECO ontology
    
    This class stores information about a ontology, such as its name, 
    the description of the ontology and the term of the ontology.
    """
    peco_id = models.CharField(max_length=50, unique=True)
    peco_name = models.CharField(max_length=200)
    extended_peco = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.peco_name