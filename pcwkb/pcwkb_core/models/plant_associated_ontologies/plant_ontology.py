from django.db import models

class PlantOntologyTerm(models.Model):
    po_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_values_as_dict(self):
        new_dict = {
            'po_id' : self.po_id,
            'name' : self.name,
            'description': self.description,
            'model_name' : 'PlantOntologyTerm',
        }
        return new_dict


class PlantComponent(models.Model):
    name = models.CharField('Plant Anatomy name (based on Plant Ontology)',
                            max_length=30)
    plant_anatomy_po = models.CharField('Plant Anatomy PO Identifier',
                                        max_length=12)
    description = models.TextField('Description of plant structure',
                                   max_length=2000)

    def get_values_as_dict(self):
        new_dict = {
            'name' : self.name,
            'plant_anatomy_po': self.plant_anatomy_po,
            'description': self.description,
            'model_name' : 'Plant Component',
        }
        return new_dict

        

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

    def get_values_as_dict(self):
        new_dict = {
            'plant_dev_stage_po' : self.plant_dev_stage_po,
            'dev_stage_name_po': self.dev_stage_name_po,
            'description': self.description,
            'model_name' : 'Plant Component Development Stage',
        }
        return new_dict

    def __str__(self):
        return self.description