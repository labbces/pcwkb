from django.db import models

class TemporaryData(models.Model):
    taxid = models.IntegerField(label="Plant TaxID")
    plant_name = models.CharField(label="Plant's scientific name", required=True)
    plant_image = models.ImageField(label="Plant image")
    plant_image_source = models.URLField(label="Image Source URL")
    description = models.CharField(label="Plant description", max_length=200, required=True)

    class Meta:
        managed = False  # Não cria uma tabela no banco de dados principal
        db_table = 'temporary_data'  # Nome da tabela temporária