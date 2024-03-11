from django.db import models

from pcwkb_core.utils.ontologies.obo_related import Parser


class ChEBI(models.Model):
    """Receive ChEBI information
    
    This class stores information about a ChEBI component, such as its name, 
    the description and the ID of ChEBI.
    """
    name = models.CharField(max_length=100)
    chebi_id = models.CharField(max_length=100)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def add_chebi(filename):
        """TODO: Import OBO file from ChEBIs
        """
        
        pronto_obo = Parser(filename)

    
        return
