from django.db import models
from .models import GeneOntologyTerm

class Gene(models.Model):
    gene_id = models.CharField(max_length=50, unique=True)
    gene_name = models.CharField(max_length=100)
    description = models.TextField()('self', on_delete=models.SET_NULL, null=True, blank=True)
    original_db = models.CharField(max_length=50, unique=True)
    go = models.ForeignKey(GeneOntologyTerm, on_delete=models.CASCADE)

    def __str__(self):
        return self.gene_name

    def get_values_as_dict(self):
        new_dict = {
            'gene_id' : self.gene_id,
            'name' : self.gene_name,
            'description': self.description,
            'original_db': self.original_db,
            'go': self.go 
            'model_name' : 'Gene',
        }
        return new_dict
