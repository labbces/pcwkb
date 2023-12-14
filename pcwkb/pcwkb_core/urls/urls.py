from django.urls import path
from django.urls import path, include

from pcwkb_core.views import base_views
from pcwkb_core.views.taxonomy import species
from pcwkb_core.views.molecular_components import gene

urlpatterns = [
    path("browse_species", species.browse_species, name='browse_species'),
    path("species_page/<str:species_code>", species.species_page, name='species_page'),
    path("gene_page/<int:gene_id>", gene.gene_page, name='gene_page'),
    path('', base_views.index, name='index'),
    path('team', base_views.team, name='team'),
    path('funding', base_views.funding, name='funding'),
    path('faq', base_views.faq, name='faq'),
    path('search/search', include('haystack.urls')),
]