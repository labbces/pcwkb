from django.db import models

class TemporaryData(models.Model):

    class Meta:
        managed = False  # Não cria uma tabela no banco de dados principal
        db_table = 'temporary_data'  # Nome da tabela temporária