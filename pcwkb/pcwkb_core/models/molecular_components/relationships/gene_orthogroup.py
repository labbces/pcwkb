from django.db import models
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
from pcwkb_core.models.molecular_components.relationships.orthogroups import Orthogroup

class GeneOrthogroup(models.Model):
    orthogroup = models.ForeignKey(Orthogroup, on_delete=models.CASCADE)
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.protein.protein_name}_{self.orthogroup.orthogroup_id}.{self.orthogroup.og_method}"
        

    