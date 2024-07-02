from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm
from pcwkb_core.models.biomass.plant_trait import PlantTrait
from pcwkb_core.models.biomass.cellwall_component import CellWallComponent
from pcwkb_core.models.biomass.plant_component import PlantComponent
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class BiomassGeneExperimentAssoc(models.Model):
    experiment_species = models.ForeignKey(Species, on_delete=models.CASCADE, null=True, blank=True) #explicar melhor
    plantcomponent = models.ManyToManyField(PlantComponent, blank=True)  
    cellwall_component = models.ForeignKey(CellWallComponent, on_delete=models.CASCADE)  
    experiment = models.ManyToManyField(Experiment)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE) 
    plant_trait = models.ForeignKey(PlantTrait, on_delete=models.CASCADE, null=True, blank=True)  
    gene_expression = models.CharField("Gene expression",max_length=100, null=True, blank=True)
    effect_on_plant_cell_wall_component = models.CharField("Effect on plant", max_length=100)

    def __str__(self):
        return f"{self.experiment}_{self.experiment_species}_{self.to or 'N/A'}"
    
#uma tabela para cada categoria
#checar o tipo
class RelationshipsExpressionExperiment(models.Model):
    expression = models.CharField(max_length=100)
    biomass_gene_experiment_assoc  = models.ForeignKey(BiomassGeneExperimentAssoc, on_delete=models.CASCADE)

    def __str__(self):
        return self.expression

class RelationshipsMutationExperiment(models.Model): #(knockout tá dentro de mutação)
    mutation = models.CharField(max_length=100)
    effect_on_gene = models.CharField(max_length=100)
    biomass_gene_experiment_assoc  = models.ForeignKey(BiomassGeneExperimentAssoc, on_delete=models.CASCADE)

    def __str__(self):
        return self.mutation