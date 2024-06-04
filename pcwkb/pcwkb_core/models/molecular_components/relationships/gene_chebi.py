from django.db import models

from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class GeneGenome(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    chebi = models.ForeignKey(ChEBI, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gene}_{self.chebi}"