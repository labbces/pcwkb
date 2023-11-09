from django.db import models

class Protein(models.Model):
    protein_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_values_as_dict(self):
        new_dict = {
            'name' : self.name,
            'protein_id': self.protein_id,
            'description': self.description,
            'model_name' : 'Protein',
        }
        return new_dict
