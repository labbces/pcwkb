from django.db import models
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm
from pcwkb_core.models.ontologies.plant_related.to import TOTerm
from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene

class Experimentalevidenceplanttrait(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    po = models.ForeignKey(PlantOntologyTerm, on_delete=models.CASCADE)
    chebi = models.ForeignKey(ChEBI, on_delete=models.CASCADE, null=True, blank=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    to = models.ForeignKey(TOTerm, on_delete=models.CASCADE)
    effect = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.model_name:  # Gerar og_name somente se não estiver definido
            self.model_name = f"{self.experiment}_{self.species}_{self.to}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.model_name