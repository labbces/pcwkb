from django.contrib import admin

from .models.taxonomy.ncbi_taxonomy import Species
from .models.molecular_components.genetic_components.genes import Gene
from .models.molecular_components.genetic_components.genomes import Genome
from .models.biomass.biomass_composition import BiomassComposition
from .models.literature.literature import Literature

admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(Genome)
admin.site.register(BiomassComposition)
admin.site.register(Literature)
