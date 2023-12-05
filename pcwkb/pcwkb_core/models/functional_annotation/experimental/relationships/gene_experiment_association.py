from django.db import models

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature


class GeneExperimentAssociation(models.Model):
    """TODO: documentation
    
    """

    gene_id = models.ForeignKey(Gene, on_delete=models.CASCADE)
    experiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    literature_id = models.ForeignKey(Literature, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.annotation_method

