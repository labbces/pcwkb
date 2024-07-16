from django.db import models
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
from pcwkb_core.models.functional_annotation.computational.annotation_method import AnnotationMethod

class MetabolicMap(models.Model):
    """Receive Metabolic map informations
    
    This class stores information about metabolic pathways, 
    such as its name, the KEGG ID related to the map, the map
    class, the KO pathway entry and the description of the KEGG map.
    """
    kegg_map_id = models.CharField('KEGG map identifier', max_length=8)
    name = models.CharField('Map name', max_length=30)
    map_class = models.CharField('Map class', max_length=100)
    kegg_pathway = models.CharField('KO pathway entry', max_length=7)
    description = models.TextField('KEGG map description', max_length=4000)

    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)

    def __str__(self):
        return self.kegg_map_id
    
class KeggOrtholog(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    kegg_ortholog = models.CharField('Kegg Ortholog', max_length=30)
    metabolic_map = models.ManyToManyField("MetabolicMap")
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.kegg_ortholog