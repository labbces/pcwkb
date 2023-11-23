from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.literature.literature import Literature

class Genome(models.Model):
    genome_version = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    source_db = models.CharField(max_length=50)

    literature_id = models.ForeignKey(Literature, on_delete=models.CASCADE)
    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.genome_version