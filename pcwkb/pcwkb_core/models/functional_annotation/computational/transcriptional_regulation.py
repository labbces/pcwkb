from django.db import models
from pcwkb_core.models.functional_annotation.computational.annotation_method import GenomeAnnotationMethod


class TranscriptionalRegulatorFamily(models.Model):
    """Relates the regulator  family
    
    This class stores information about the regulators
    class and the regulator familym a foreing key from
    the class GenomeAnnotationMethod, so it can be associated
    to show the transcriptional regulator family.
    """
    regulator_class = models.CharField('Regulator class', max_length=20)
    family = models.CharField('Regulator family', max_length=20)

    def __str__(self):
        return self.regulator_class


