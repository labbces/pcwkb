from django.db import models
from pcwkb_core.models.molecular_components.proteins import Protein

class MetabolicMap(models.Model):
    kegg_map_id = models.CharField('KEGG map identifier', max_length=8)
    name = models.CharField('Map name', max_length=30)
    map_class = models.CharField('Map class', max_length=100)
    ko_pathway = models.CharField('KO pathway entry', max_length=7)
    description = models.TextField('KEGG map description', max_length=4000)

    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)

    def __str__(self):
        return self.kegg_map_id