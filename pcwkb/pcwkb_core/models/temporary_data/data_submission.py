from django.db import models

class TemporaryData(models.Model):

    class Meta:
        managed = False  # Não cria uma tabela no banco de dados principal
        db_table = 'temporary_data'  # Nome da tabela temporária

class DataSubmission(models.Model):
    title = models.CharField(max_length=50)
    json_data = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)