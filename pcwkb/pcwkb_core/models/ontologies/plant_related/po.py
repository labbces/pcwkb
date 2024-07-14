from django.db import models

class PlantOntologyTerm(models.Model):
    """Receive ECO ontology
    
    This class stores information about a ontology, such as its name, 
    the description of the ontology and the term of the ontology.
    """
    po_id = models.CharField(max_length=50, unique=True)
    po_name = models.CharField(max_length=200)
    extended_po = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.po_name