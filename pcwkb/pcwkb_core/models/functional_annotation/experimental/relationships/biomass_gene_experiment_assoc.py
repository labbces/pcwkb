from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm
from pcwkb_core.models.biomass.plant_trait import PlantTrait
from pcwkb_core.models.biomass.cellwall_component import CellWallComponent
from pcwkb_core.models.biomass.plant_component import PlantComponent
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene


class GeneRegulation(models.Model):
    CONDITION_CHOICES = [
        ('KNOCKOUT', 'Knockout'),
        ('INSERTION', 'Insertion'),
        ('DELETION', 'Deletion'),
        ('POINT_MUTATION', 'Point Mutation'),
        ('SUBSTITUTION', 'Substitution'),
        ('FRAME_SHIFT', 'Frame Shift Mutation'),
        ('GENE_AMPLIFICATION', 'Gene Amplification'),
        ('GENE_FUSION', 'Gene Fusion'),
        ('TRANSLOCATION', 'Translocation'),
        ('DUPLICATION', 'Duplication'),
        ('EPIGENETIC_MOD', 'Epigenetic Modification'),
        ('OVEREXPRESSION', 'Overexpression'),
        ('GENE_SILENCING', 'Gene Silencing'),
        ('CONDITIONAL_KNOCKOUT', 'Conditional Knockout'),
        ('INSERTIONAL_MUTAGENESIS', 'Insertional Mutagenesis'),
    ]

    condition_type = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.condition_type

class BiomassGeneExperimentAssoc(models.Model):
    experiment_species = models.CharField(max_length=100, null=False, blank=True)
    plant_component = models.ManyToManyField(PlantComponent, blank=True)
    plant_cell_wall_component = models.ForeignKey(CellWallComponent, on_delete=models.CASCADE)
    experiment = models.ManyToManyField(Experiment)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    plant_trait = models.ForeignKey(PlantTrait, on_delete=models.CASCADE, null=True, blank=True)
    gene_regulation = models.ForeignKey(GeneRegulation, on_delete=models.CASCADE)
    effect_on_plant_cell_wall_component = models.CharField("Effect on plant", max_length=100)

    def __str__(self):
        return f"{self.experiment_species}_{self.plant_cell_wall_component}_{self.gene}_{self.literature}"


