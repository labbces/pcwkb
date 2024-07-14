from django.db import models

class TOTerm(models.Model):
    """Receive TO ontology
    
    This class stores information about a ontology, such as its name, 
    the description of the ontology and the term of the ontology.
    """
    to_id = models.CharField(max_length=50, unique=True)
    to_name = models.CharField(max_length=200)
    extended_to = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.to_name