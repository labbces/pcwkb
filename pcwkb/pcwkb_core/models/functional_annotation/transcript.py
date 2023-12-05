from django.db import models
from pcwkb_core.models.molecular_components.genetic_components.proteins import Protein
from pcwkb_core.models.functional_annotation.annotation_method import GenomeAnnotationMethod

class TranscriptionalRegulatorFamily(models.Model):
    regulator_class = models.CharField('Regulator class', max_length=20)
    family = models.CharField('Regulator family', max_length=20)

    def __str__(self):
        return self.regulator_class


class TranscRegProteinAssociation(models.Model):
    annotation_method = models.ForeignKey(GenomeAnnotationMethod, on_delete=models.CASCADE, null=False, blank=False)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    family = models.ForeignKey(TranscriptionalRegulatorFamily, on_delete=models.CASCADE)

    def __str__(self):
        return self.annotation_method