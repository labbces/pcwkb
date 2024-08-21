from django.db import models

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature


class GeneInterationExperimentAssociation(models.Model):
    """Relate a gene function on the PCW with an experiment 
    
    This class relates a gene with an experiment that involves
    it using the literature that brings this experiment.
    """

    putative_gene_regulator = models.ForeignKey(Gene, on_delete=models.CASCADE, related_name='regulator_association')
    gene_target = models.ForeignKey(Gene, on_delete=models.CASCADE, related_name='target_association')
    experiment = models.ManyToManyField(Experiment)
    experiment_species = models.CharField(max_length=100, null=True, blank=True)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, null=False, blank=False)
    effect_on_target = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.putative_gene_regulator}_{self.gene_target}_{self.literature}"