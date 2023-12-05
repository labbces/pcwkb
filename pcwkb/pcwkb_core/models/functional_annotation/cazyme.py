from django.db import models
from pcwkb_core.models.molecular_components.genetic_components.proteins import Protein
from pcwkb_core.models.functional_annotation.annotation_method import GenomeAnnotationMethod


class CAZyme(models.Model):
    family = models.CharField('CAZyme Family', max_length=30)
    cazyme_class = models.CharField('CAZyme Class', max_length=30)
    clan = models.CharField('CAZyme Clan', max_length=30, null=True, blank=True)
    sub_family = models.CharField('CAZyme Family', max_length=8, null=True, blank=True)
    putative_activities = models.TextField('Putative activities in Family or Subfamily', max_length=4000)

    def __str__(self):
        return self.cazyme_class
    

class CAZymeProteinAssociation(models.Model):
    annotation_method = models.ForeignKey(GenomeAnnotationMethod, on_delete=models.CASCADE, null=True, blank=True)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    family = models.ForeignKey(CAZyme, on_delete=models.CASCADE)

    def __str__(self):
        return self.annotation_method