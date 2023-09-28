from django.db import models
from .models import Species

class Genome(models.Model):
    genome_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()('self', on_delete=models.SET_NULL, null=True, blank=True)
    original_db = models.CharField(max_length=50, unique=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_values_as_dict(self):
        new_dict = {
            'genome_id' : self.genome_id,
            'name' : self.name,
            'description': self.description,
            'original_db': self.original_db,
            'species': self.species
            'model_name' : 'Genome',
        }
        return new_dict