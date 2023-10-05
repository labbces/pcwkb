from django.contrib import admin

from .models.taxonomy.ncbi_taxonomy import Species

admin.site.register(Species)
