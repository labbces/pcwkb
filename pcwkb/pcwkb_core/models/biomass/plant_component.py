from django.db import models

from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm

class PlantComponent(models.Model):
    """Receive plant cell wall information
    
    This class stores information about plant component, such as its name, 
    the description of the composition and the po ID for the components, stored in PlantOntologyTerm class.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    po = models.ForeignKey(PlantOntologyTerm, on_delete=models.CASCADE)

    def __str__(self):
        return self.name