from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm
from pcwkb_core.models.ontologies.plant_related.to import TOTerm
from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class BiomassGeneExperimentAssoc(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE) #seria obrigatório?
    po = models.ForeignKey(PlantOntologyTerm, on_delete=models.CASCADE)  #seria obrigatório?
    chebi = models.ForeignKey(ChEBI, on_delete=models.CASCADE, null=True, blank=True)  #seria obrigatório?
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE) 
    to = models.ForeignKey(TOTerm, on_delete=models.CASCADE, null=True, blank=True)  #seria obrigatório?
    gene_expression = models.CharField("Gene expression",max_length=100, null=True, blank=True)  #seria obrigatório?
    effect_on_plant_cell_wall_component = models.CharField("Effect on plant", max_length=100)  #seria obrigatório?
    model_name = models.CharField("Model name", max_length=100, blank=True)

    def __str__(self):
        return f"{self.experiment}_{self.species}_{self.to or 'N/A'}"