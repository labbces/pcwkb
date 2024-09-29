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
    
    def get_second_eco_name(self):
        """Retrieve the eco_name of the second eco_id in the extended_eco field."""
        if not self.extended_eco:
            return None
        eco_ids = self.extended_eco.split(';')
        if len(eco_ids) < 2:
            return None
        second_eco_id = eco_ids[1]
        try:
            second_eco_term = ECOTerm.objects.get(eco_id=second_eco_id)
            return second_eco_term.eco_name
        except ECOTerm.DoesNotExist:
            return None