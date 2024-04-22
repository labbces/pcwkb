from django.db import models

class ECOTerm(models.Model):
    """Receive ECO ontology
    
    This class stores information about a ontology, such as its name, 
    the description of the ontology and the term of the ontology.
    """
    eco_id = models.CharField(max_length=50, unique=True)
    eco_name = models.CharField(max_length=200)
    extended_eco = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.eco_name