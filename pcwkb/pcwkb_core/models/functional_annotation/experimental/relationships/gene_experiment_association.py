from django.db import models

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm


class GeneExperimentAssociation(models.Model):
    """Relate a gene function on the PCW with an experiment 
    
    This class relates a gene with an experiment that involves
    it using the literature that brings this experiment.
    """

    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    po = models.ForeignKey(PlantOntologyTerm, on_delete=models.CASCADE)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, null=False, blank=False)
    effect = models.CharField(max_length=100)
    #variedade
    #condição experimental
    

    def __str__(self):
        return self.annotation_method

