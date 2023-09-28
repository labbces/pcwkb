from django.db import models

class GeneOntologyTerm(models.Model):
    term_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_values_as_dict(self):
        new_dict = {
            'name' : self.name,
            'term_id': self.term_id,
            'description': self.description,
            'model_name' : 'GeneOntologyTerm',
        }
        return new_dict
