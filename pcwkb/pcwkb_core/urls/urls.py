from django.urls import path
from django.urls import path, include

from pcwkb_core.views import base_views
from pcwkb_core.views.taxonomy import species
from pcwkb_core.views.molecular_components import gene
from pcwkb_core.views.forms import data_submission
from pcwkb_core.views.forms import species_submission
from pcwkb_core.views.relationships import orthogroup
from pcwkb_core.views.experiment import experiment

urlpatterns = [
    path('browse_species', species.browse_species, name='browse_species'),
    path('species_page/<str:species_code>', species.species_page, name='species_page'),
    path('gene_page/<str:gene_name>', gene.gene_page, name='gene_page'),
    path('gene_list/<int:species_id>', gene.paginated_gene_list, name='gene_list'),
    path('og_page/<str:og_name>', orthogroup.og_page, name='og_page'),
    path('', base_views.index, name='index'),
    path('team', base_views.team, name='team'),
    path('funding', base_views.funding, name='funding'),
    path('faq', base_views.faq, name='faq'),    
    #path('search/', include('haystack.urls')),
    path('search_results/', base_views.search, name='search'),
    path('data_submission', data_submission.get_data_file, name='data_submission'),
    path('species_submission', species_submission.get_data_file, name='data_submission'),
    path('ontologies', base_views.ontologies, name='ontologies'),
    path('experiment_page/<str:experiment_name>', experiment.exp_page, name='experiment_page'),
    path('experiment_form', data_submission.experiment_form_view, name='experiment_form'),
]