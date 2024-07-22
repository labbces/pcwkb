from django.db import models
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
from pcwkb_core.models.functional_annotation.computational.annotation_method import AnnotationMethod

class GeneOntologyTerm(models.Model):
    """Receive Gene Ontology terms
    
    This class stores information about a ontology, such as its name, 
    the description of the ontology and the term of the ontology.
    """

    go_id = models.CharField(max_length=50, unique=True)
    go_name = models.CharField(max_length=50, unique=True)
    extended_go = models.TextField(null=True, blank=True)
    go_class = models.CharField(max_length=200, null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.go_term  

class GeneOntologyProteinAssociation(models.Model):
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.CASCADE, null=True, blank=True)
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    go_term = models.ForeignKey(GeneOntologyTerm, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.protein}_{self.go_term}_{self.annotation_method}"