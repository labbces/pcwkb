from django.db import models


class Transcript(models.Model):
    """TODO: documentation
    
    """
    sequence = models.TextField('Trancript sequence', max_length=12000)

    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

    def __str__(self):
        return self.sequence