from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.literature.literature import Literature

class BiomassComposition(models.Model):
    """TODO: documentation
    """
    components_percentage = models.JSONField(null=True, blank=True)

    literature_id = models.ForeignKey(Literature, on_delete=models.CASCADE)
    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)