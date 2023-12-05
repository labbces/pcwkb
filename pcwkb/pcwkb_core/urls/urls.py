from django.urls import path
from django.urls import path, include

from pcwkb.pcwkb_core.views.taxonomy import species
from pcwkb.pcwkb_core.views.molecular_components import gene

urlpatterns = [
    path("", species.index, name="index"),
    path("browse_species", species.browse_species, name='browse_species'),
    path("species_page/<str:species_code>", species.species_page, name='species_page'),
    path("gene_page/<int:gene_id>", gene.gene_page, name='gene_page'),
    path('team', species.team, name='team'),
    path('funding', species.funding, name='funding'),
    path('faq', species.faq, name='faq'),
    path('search/search', include('haystack.urls')),
]