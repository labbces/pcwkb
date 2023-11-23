from django.db import models
from pcwkb_core.models.molecular_components.proteins import Protein

class GeneOntologyTerm(models.Model):
    go_id = models.CharField(max_length=50, unique=True)
    go_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.go_name


class GOProteinAssociation(models.Model):
    go_id = models.ForeignKey(GeneOntologyTerm, on_delete=models.CASCADE)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)

