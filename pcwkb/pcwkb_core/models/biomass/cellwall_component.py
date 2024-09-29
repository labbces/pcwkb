from django.db import models

from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI

class CellWallComponent(models.Model):
    """Receive plant cell wall information
    
    This class stores information about plant cell wall composition, such as its name, 
    the description of the composition and the ChEBI ID for the components, stored in ChEBI class.
    """
    cellwallcomp_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    chebi = models.ForeignKey(ChEBI, on_delete=models.CASCADE)
    #kegg = models.ForeignKey(KeggCompound)

    def __str__(self):
        return self.cellwallcomp_name
    
    def add_from_chebi(chebi_name):
        """ Gets CellWall Component information using the chebi identifier from the chebi model.

        Verify if chebi already exists in the CellWallComponents objects, if not, collect data and store in the fields from this class.
        """

        try:
            chebi = ChEBI.objects.get(chebi_name=chebi_name)
        except:
            return "chebi_id incorrect"
        try:
            cellwall_component = CellWallComponent.objects.get(chebi=chebi)
            return cellwall_component
        except:
            new_cell_wall_component = CellWallComponent.objects.create(cellwallcomp_name=chebi.chebi_name,
                                                           description=chebi.definition,
                                                           chebi=chebi)
            return new_cell_wall_component