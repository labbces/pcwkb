from django.db import models
from pcwkb_core.models.functional_annotation.computational.annotation_method import GenomeAnnotationMethod


class TranscriptionalRegulatorFamily(models.Model):
    regulator_class = models.CharField('Regulator class', max_length=20)
    family = models.CharField('Regulator family', max_length=20)

    def __str__(self):
        return self.regulator_class


