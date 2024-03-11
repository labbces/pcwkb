from django.db import models

class SpeciesTemporaryData(models.Model):
    taxid = models.IntegerField("Plant TaxID")
    plant_name = models.CharField("Plant's scientific name", max_length=200, null=False)
    plant_image_source = models.URLField("Image Source URL")
    description = models.CharField("Plant description", max_length=200, null=False)

    class Meta:
        managed = False  # Não cria uma tabela no banco de dados principal
        db_table = 'temporary_data'  # Nome da tabela temporária