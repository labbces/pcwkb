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
        ('UPREGULATION', 'upregulation'),
        ('DOWNREGULATION', 'downregulation'),
        ('KNOCKOUT', 'knockout'),
        ('INSERTION', 'insertion'),
        ('DELETION', 'deletion'),
        ('POINT_MUTATION', 'point mutation'),
        ('SUBSTITUTION', 'substitution'),
        ('FRAME_SHIFT', 'frame shift mutation'),
        ('GENE_AMPLIFICATION', 'gene amplification'),
        ('GENE_FUSION', 'gene fusion'),
        ('TRANSLOCATION', 'translocation'),
        ('DUPLICATION', 'duplication'),
        ('EPIGENETIC_MOD', 'epigenetic modification'),
        ('OVEREXPRESSION', 'overexpression'),
        ('GENE_SILENCING', 'gene silencing'),
        ('CONDITIONAL_KNOCKOUT', 'conditional knockout'),
        ('INSERTIONAL_MUTAGENESIS', 'insertional mutagenesis'),
    ]

    condition_type = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_condition_type_display()

class BiomassGeneExperimentAssoc(models.Model):
    experiment_species = models.CharField(max_length=100, null=False, blank=False)
    experiment_species_variety = models.CharField(max_length=100, null=True, blank=True)
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


