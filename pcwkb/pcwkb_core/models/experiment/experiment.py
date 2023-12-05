from django.db import models
from pcwkb_core.models.experiment.eco import ECOTerm
from pcwkb_core.models.literature.literature import Literature

class Experiment(models.Model):
    experiment_id = models.CharField(max_length=50, unique=True)
    experiment_name = models.CharField(max_length=50)
    experiment_category = models.CharField('Category of the experiment', max_length=50)
    description = models.TextField(null=True, blank=True)

    eco_term = models.ForeignKey(ECOTerm, on_delete=models.CASCADE, null=True, blank=True)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.experiment_name