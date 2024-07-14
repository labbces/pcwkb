from django.db import models

from pcwkb_core.models.ontologies.experiment_related.eco import ECOTerm
from pcwkb_core.models.ontologies.plant_related.peco import PECOTerm
from pcwkb_core.models.literature.literature import Literature


class Experiment(models.Model):
    """Receive an experiment involving PCW related genes.
    
    This class stores information about an experiment, such as its name, 
    the description of the experiment and the experiment category. It also
    can recieve a ECO Term and is required to com with a literature to validate
    the experiment. 2
    """
    experiment_name = models.CharField(max_length=50)
    experiment_category = models.CharField('Category of the experiment', max_length=50)
    description = models.TextField(null=True, blank=True)

    peco_term = models.ForeignKey(PECOTerm, on_delete=models.CASCADE, null=True, blank=True)
    eco_term = models.ForeignKey(ECOTerm, on_delete=models.CASCADE, null=True, blank=True)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.experiment_name