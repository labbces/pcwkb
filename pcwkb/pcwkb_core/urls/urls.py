from django.urls import path
from django.urls import path, include

from pcwkb_core.views import base_views
from pcwkb_core.views.taxonomy import species
from pcwkb_core.views.molecular_components import gene
from pcwkb_core.views.forms import data_submission
from pcwkb_core.views.forms import species_submission
from pcwkb_core.views.relationships import orthogroup
from pcwkb_core.views.experiment import experiment
from pcwkb_core.views.cellwallcomponent import cellwallcomponent
from pcwkb_core.views import accounts
from pcwkb_core.views.search import search_view

urlpatterns = [
    path('browse_species', species.browse_species, name='browse_species'),
    path('species_page/<str:species_code>', species.species_page, name='species_page'),
    path('gene_page/<str:gene_name>', gene.gene_page, name='gene_page'),
    path('gene_list/<int:species_id>', gene.paginated_gene_list, name='gene_list'),
    path('gene_biomass_list/<int:species_id>', gene.paginated_gene_experiment_list, name='gene_biomass_list'),
    path('og_page/<str:og_name>', orthogroup.og_page, name='og_page'),
    path('', base_views.index, name='index'),
    path('team', base_views.team, name='team'),
    path('funding', base_views.funding, name='funding'),
    path('faq', base_views.faq, name='faq'),    
    path('search/', include('haystack.urls')),
    path('search_pcwkb/', search_view.search_pcwkb, name='search_pcwkb'),
    path('search_engine/', base_views.search_engine, name='search_engine'),
    path('autocomplete/', base_views.autocomplete, name='autocomplete'),
    path('data_submission', data_submission.data_submission_view, name='data_submission'),
    path('species_submission', species_submission.get_data_file, name='species_submission'),
    path('ontologies', base_views.ontologies, name='ontologies'),
    path('experiments', experiment.experiment, name='experiments'),
    path('experiment_page/<str:experiment_name>', experiment.exp_page, name='experiment_page'),
    path('cellwallcomponents', cellwallcomponent.cellwallcomponent, name='cellwallcomponents'),
    path('cellwallcomponent_page/<str:chebi_name>', cellwallcomponent.cell_wall_comp_page, name='cellwallcomponent_page'),
    path('experiment_form', data_submission.experiment_form_view, name='experiment_form'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registration', accounts.registration, name='registration'),
]