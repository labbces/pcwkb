from django.shortcuts import render, get_object_or_404
import requests

from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc
from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI

def cellwallcomponent(request):

    context={"cellwallcomponents":{}}

    for info in BiomassGeneExperimentAssoc.objects.all():
        chebi_name = info.chebi.chebi_name
        context["cellwallcomponents"][chebi_name] = {
            "definition": info.chebi.definition,
            "chebi_id": info.chebi.chebi_id
        }

    return render(request, 'cellwallcomponents.html',  context)

def cell_wall_comp_page(request, chebi_name):
    context = {}
    
    cellwallcomponent = get_object_or_404(ChEBI, chebi_name=chebi_name)
    biomass_gene_assocs = cellwallcomponent.biomassgeneexperimentassoc_set.all()

    if biomass_gene_assocs.exists():
        assoc_list = {'species': [], 'genes': [], 'genes_count': 0, 'species_count': 0}

        for assoc in biomass_gene_assocs:
            assoc_list['species'].append(assoc.gene.species)
            assoc_list['genes'].append(assoc.gene)

        assoc_list['genes_count'] = len(assoc_list['genes'])
        assoc_list['species_count'] = len(assoc_list['species'])

    else:
        assoc_list = None

    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{chebi_name}"
    response = requests.get(wiki_url)
    if response.status_code == 200:
        wikipedia_content = response.json()
    else:
        wikipedia_content = {"extract_html": "We are unable to retrieve the Wikipedia information for this entry at this time. Please try again later."}

    context.update({
        "cellwallcomponent": cellwallcomponent,
        "assoc_list": assoc_list,
        "wikipedia_content": wikipedia_content,
    })

    return render(request, 'relationships/cell_wall_component.html', context)
