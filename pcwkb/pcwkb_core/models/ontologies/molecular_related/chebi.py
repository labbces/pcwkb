from django.db import models

from pcwkb_core.utils.ontologies.obo_related import read_obo


class ChEBI(models.Model):
    """
    
    """
    name = models.CharField(max_length=100)
    chebi_id = models.CharField(max_length=100)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def add_chebi(filename):
        """TODO: Import OBO file from ChEBI
        
        """
        
        pronto_obo = read_obo(filename)

        


        return
