from django.db import models

class PlantOntologyTerm(models.Model):
    """Receive ECO ontology
    
    This class stores information about a ontology, such as its name, 
    the description of the ontology and the term of the ontology.
    """
    po_id = models.CharField(max_length=50, unique=True)
    po_name = models.CharField(max_length=200)
    extended_po = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.po_name

class PlantComponent(models.Model):
    name = models.CharField('Plant Anatomy name (based on Plant Ontology)',
                            max_length=30)
    plant_anatomy_po = models.CharField('Plant Anatomy PO Identifier',
                                        max_length=12)
    description = models.TextField('Description of plant structure',
                                   max_length=2000)

        

class PlantComponentDevStage(models.Model):
    plant_dev_stage_po = models.CharField('Plant Structure Development Stage PO Identifier',
                                        max_length=12,
                                        null=True,
                                        blank=True)
    dev_stage_name_po = models.TextField('Plant Structure Development Stage PO Name',
                                        max_length=2000,
                                        null=True,
                                        blank=True)
    description = models.TextField('Description of plant dev stage (PO Definition)',
                                   max_length=2000,
                                   null=False,
                                   blank=False)

    def __str__(self):
        return self.description