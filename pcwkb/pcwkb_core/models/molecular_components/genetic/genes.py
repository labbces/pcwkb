from django.db import models

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genomes import Genome
from pcwkb_core.models.literature.literature import Literature

class Gene(models.Model):
    
    """Receive genes information
    
    This class stores information about a gene, such as its name, 
    the description of the gene and the database where this gene was found. 
    We also require that this gene need to be related to a species, reason 
    why we included the cascade ForeingKey. 
    """

    gene_name = models.CharField(max_length=100, null=True, blank=True) #gene name
    gene_id = models.CharField(max_length=100, null=True, blank=True) #gene identifier
    description = models.TextField(blank=True, null=True) #gene description
    original_db_info = models.CharField(max_length=50, blank=True, null=True) #Gene information db source (E.g. Phytozome)
    species = models.ForeignKey(Species, on_delete=models.CASCADE) # Species the gene belongs to
    species_variety = models.CharField(max_length=50, blank=True, null=True) #Plant variety
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE, blank=True, null=True) #Genome where the gene came from
    name_id_assoc_source_lit = models.ForeignKey(Literature, on_delete=models.CASCADE, blank=True, null=True) #Source that linked the gene identifier with the gene name
    name_id_assoc_source_site = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.gene_name
