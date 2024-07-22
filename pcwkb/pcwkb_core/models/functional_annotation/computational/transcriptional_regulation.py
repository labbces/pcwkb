from django.db import models
from pcwkb_core.models.functional_annotation.computational.annotation_method import AnnotationMethod
from pcwkb_core.models.molecular_components.genetic.genes import Gene


class TranscriptionalRegulatorFamily(models.Model):
    """Relates the regulator  family
    
    This class stores information about the regulators
    class and the regulator family a foreing key from
    the class AnnotationMethod, so it can be associated
    to show the transcriptional regulator family.
    """
    regulator_class = models.CharField('Regulator class', max_length=20)
    family = models.CharField('Regulator family', max_length=20)

    def __str__(self):
        return self.regulator_class

class GeneTFAssociation(models.Model):
    """Relates a gene with its function 
    
    This class associates the anotation method, 
    the gene and the transcriptional regulatory family.
    """
    
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.CASCADE, null=False, blank=False)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    transcriptionalregulatorfamily = models.ForeignKey(TranscriptionalRegulatorFamily, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.gene}_{self.transcriptionalregulatorfamily}_{self.annotation_method}"


