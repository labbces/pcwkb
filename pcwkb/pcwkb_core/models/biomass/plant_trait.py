from django.db import models

from pcwkb_core.models.ontologies.plant_related.to import TOTerm

class PlantTrait(models.Model):
    """Receive plant cell wall information
    
    This class stores information about plant trait, such as its name, 
    the description of the composition and the po ID for the components, stored TOTerm class.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    to = models.ForeignKey(TOTerm, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def add_from_to(to_name):
        """ Gets Plant Trait information using the trait ontology (to) identifier from the TOTerm model.

        Verify if to already exists in the PlantTrait objects, if not, collect data and store in the fields from this class.
        """

        try:
            to = TOTerm.objects.get(to_name=to_name)
        except:
            return "to_id incorrect"
        try:
            plant_trait = PlantTrait.objects.get(to=to)
            return plant_trait
        except:
            new_plant_trait = PlantTrait.objects.create(name=to.to_name,
                                                           description=to.definition,
                                                           to=to)
            return new_plant_trait