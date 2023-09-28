from django.db import models

class PECOTerm(models.Model):
    peco_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_values_as_dict(self):
        new_dict = {
            'peco_id' : self.peco_id,
            'name' : self.name,
            'description': self.description,
            'model_name' : 'PECOTerm',
        }
        return new_dict