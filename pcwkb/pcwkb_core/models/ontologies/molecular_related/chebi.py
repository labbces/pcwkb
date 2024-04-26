from django.db import models

from pcwkb_core.utils.parsers.obo_related import Parser as OBOParser


class ChEBI(models.Model):
    """Receive ChEBI information
    
    This class stores information about a ChEBI component, such as its name, 
    the description and the ID of ChEBI.
    """
    chebi_id = models.CharField(max_length=50, unique=True)
    chebi_name = models.TextField('Chebi name')
    extended_chebi = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.chebi_name
2