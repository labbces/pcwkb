from django.db import models

from pcwkb_core.models.molecular_components.genetic.genomes import Genome
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class GeneGenome(models.Model):
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    gene_position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.genome}_{self.gene}"