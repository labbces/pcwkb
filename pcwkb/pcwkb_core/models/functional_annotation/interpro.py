from django.db import models
from pcwkb_core.models.molecular_components.genetic_components.proteins import Protein

class InterPro(models.Model):
    interpro_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.interpro_id


class InterProProteinAssociation(models.Model):
    interpro_id = models.ForeignKey(InterPro, on_delete=models.CASCADE)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)