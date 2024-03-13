from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm

class BiomassComposition(models.Model):
    """Receive biomass composition information
    
    This class stores information about the biomass composition, 
    wich will be recieved in a JSON file as percentage from each component.
    We also require that this gene need to be related to a specie and a literature, reason 
    why we included the cascade ForeingKey. 
    """
    components_percentage = models.JSONField(null=True, blank=True)
    po = models.ForeignKey(PlantOntologyTerm, on_delete=models.CASCADE, null=True)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.species} {self.po} Composition"

