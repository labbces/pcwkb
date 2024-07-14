from django.db import models

from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm

class PlantComponent(models.Model):
    """Receive plant cell wall information
    
    This class stores information about plant component, such as its name, 
    the description of the composition and the po ID for the components, stored in PlantOntologyTerm class.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    po = models.ManyToManyField(PlantOntologyTerm)

    def __str__(self):
        return self.name
    
    def add_from_po(po_name):
        """ Gets CellWall Component information using the po identifier from the po model.

        Verify if po already exists in the CellWallComponents objects, if not, collect data and store in the fields from this class.
        """

        try:
            po = PlantOntologyTerm.objects.get(po_name=po_name)
        except:
            return "po_name incorrect"
        try:
            plant_component = PlantComponent.objects.get(po=po)
            return f"Plant component already in the db {plant_component}"
        except:
            new_plant_component = PlantComponent.objects.create(name=po.po_name,
                                                           description=po.definition)
            new_plant_component.po.set([po])
            return new_plant_component