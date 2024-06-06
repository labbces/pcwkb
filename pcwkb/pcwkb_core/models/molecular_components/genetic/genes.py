from django.db import models

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species


class Gene(models.Model):
    """Receive genes information
    
    This class stores information about a gene, such as its name, 
    the description of the gene and the database where this gene was found. 
    We also require that this gene need to be related to a species, reason 
    why we included the cascade ForeingKey. 
    """
    gene_name = models.CharField(max_length=100, unique=True, null=True, blank=True) #unicoF
    gene_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(blank=True) 
    original_db = models.CharField(max_length=50, blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    source = models.CharField(max_length=100, blank=True) #gff3, individual study, etc.

    def __str__(self):
        return self.gene_name
