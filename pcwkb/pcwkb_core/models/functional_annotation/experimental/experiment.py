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
    experiment_name = models.CharField(max_length=100)
    experiment_category = models.CharField('Category of the experiment', max_length=50, null=True, blank=True)
    description = models.TextField('Experiment description')

    peco_term = models.ForeignKey(PECOTerm, on_delete=models.CASCADE, null=True, blank=True)
    eco_term = models.ForeignKey(ECOTerm, on_delete=models.CASCADE, null=True, blank=True)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.experiment_name
    
    def add_from_eco(eco_id):

        """Adds an experiment based on an ECO term."""

        try:
            eco_term = ECOTerm.objects.get(eco_id=eco_id)
        except ECOTerm.DoesNotExist:
            return "ECO term not found"

        experiment_category = eco_term.get_second_eco_name()

        try:
            experiment = Experiment.objects.get(eco_term=eco_term)
            return f"Experiment already in the database: {experiment}"
        except Experiment.DoesNotExist:
            new_experiment = Experiment.objects.create(
                experiment_name=eco_term.eco_name,
                experiment_category=experiment_category,  # This will be None if no second eco_name is found
                description=eco_term.definition,
                eco_term=eco_term
            )
            return new_experiment