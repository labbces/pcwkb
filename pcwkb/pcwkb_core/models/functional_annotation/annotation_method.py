from django.db import models
from pcwkb_core.models.literature.literature import Literature


class GenomeAnnotationMethod(models.Model):
    software = models.CharField('Software name', max_length=20)
    software_version = models.CharField('Software version', max_length=10)
    release_date = models.DateField('Release date')

    literature = models.ForeignKey(LiteratureItem, on_delete=models.CASCADE)