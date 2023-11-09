from django.contrib import admin

from .models.taxonomy.ncbi_taxonomy import Species
from .models.molecular_components.genetic_components.genes import Gene

admin.site.register(Species)
admin.site.register(Gene)
