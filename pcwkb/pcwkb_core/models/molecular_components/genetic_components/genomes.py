from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genes import Gene

class Genome(models.Model):
    genome_id = models.CharField(max_length=50, unique=True)
    genome_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    original_db = models.CharField(max_length=50, unique=True)

    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
    gene_id = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.genome_name