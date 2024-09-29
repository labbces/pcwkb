from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.literature.literature import Literature

class Genome(models.Model):
    """Receive genomes information
    
    This class stores information about a genome, such as its version, 
    the description of the genome and the source  database where this gene was found. 
    We also require that this gene need to be related to a specie and a literature that 
    explain about the genome assembly, reason why we included the cascade ForeingKey. 
    """
    version = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    source_db = models.CharField(max_length=50)
    genome_size = models.CharField(max_length=50)
    coding_genes_count = models.CharField(max_length=50)
    coding_transcripts_count = models.CharField(max_length=50)
    variety = models.CharField(max_length=50, blank=True, null=True)

    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.species}.{self.version}"