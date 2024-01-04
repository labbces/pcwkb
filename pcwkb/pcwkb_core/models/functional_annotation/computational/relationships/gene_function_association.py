from django.db import models

from pcwkb_core.models.molecular_components.genetic.genes import Gene



class GeneFunctionAssociation(models.Model):
    """Relates a gene with its function 
    
    This class associates the anotation method, 
    the gene and the transcriptional regulatory family.
    """

    annotation_method = models.ForeignKey(GenomeAnnotationMethod, on_delete=models.CASCADE, null=False, blank=False)
    gene_id = models.ForeignKey(Gene, on_delete=models.CASCADE)
    family = models.ForeignKey(TranscriptionalRegulatorFamily, on_delete=models.CASCADE)

    def __str__(self):
        return self.annotation_method