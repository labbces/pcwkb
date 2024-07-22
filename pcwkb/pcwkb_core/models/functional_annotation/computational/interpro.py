from django.db import models
from pcwkb_core.models.functional_annotation.computational.annotation_method import AnnotationMethod
from pcwkb_core.models.molecular_components.genetic.proteins import Protein

class InterPro(models.Model):
    """Receive InterPro information
    
    This class stores information found in InterPro, such as its ID and 
    its description.
    """
    interpro_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.interpro_id
    
class ProteinInterproAssociation(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    interpro = models.ForeignKey(InterPro, on_delete=models.CASCADE)
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.protein}_{self.interpro}"

class ProteinInterproSourceInfo(models.Model):
    protein_interpro_assoc = models.ForeignKey(ProteinInterproAssociation, on_delete=models.CASCADE, null=True, blank=True)
    ipr_source_db =  models.CharField(max_length=50)
    start = models.IntegerField("start")
    stop = models.IntegerField("stop")

    def __str__(self):
        return f"{self.protein_interpro_assoc}_{self.ipr_source_db}"