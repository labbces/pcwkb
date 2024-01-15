from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import Http404

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation

def listing_genes(species_id):
    gene_list = Gene.objects.filter(species_id=species_id)
    paginator = Paginator(gene_list, 3)  # Show 3 genes per page.

    return paginator

def species_page(request, species_code):
    """
    This function shows the species page with the species information
    that will be taken from the database using the species code.
    """

    try:
        p = Species.objects.get(species_code=species_code).id
    except Species.DoesNotExist:
        raise Http404("Species does not exist")

    context = { 'species_code': species_code,
                'species_id': '',
                'scientific_name': '',
                'common_name': '',
                'experimental_genes': {},
                'genes_paginated': {},
                'biomass_composition': "asdasdasd"}

    context['species_id'] = Species.objects.get(species_code=species_code).id
    context['genes_paginated'] = listing_genes(context['species_id'])
    print(context['genes_paginated'].page(1),'\n\n\n\n\n\n')

    context['common_name'] = Species.objects.get(species_code=species_code).common_name
    context['scientific_name'] = Species.objects.get(species_code=species_code).scientific_name
    
    return render(request, 'species/species_page.html', context)

def browse_species(request):
    """
    Function that shows a cladogram in the browse species page,
    that gets the information from the database and shows in the tree.
    """
    species_data = Species.objects.values('species_code', 'scientific_name', 'common_name', 'family', 'clade', 'photosystem')
    print(species_data)

    data = {"name": "clado", "children": []}

    clade_dict = {}
    for species in species_data:
        clade_name = species['clade']
        family_name = species['family']

        if clade_name not in clade_dict:
            clade_dict[clade_name] = {"name": clade_name, "children": []}

        family_node = next((fam for fam in clade_dict[clade_name]["children"] if fam["name"] == family_name), None)

        if family_node is None:
            family_node = {"name": family_name, "children": []}
            clade_dict[clade_name]["children"].append(family_node)

        family_node["children"].append({"name": f"{species['scientific_name']} ({species['species_code']})"})

    data["children"] = list(clade_dict.values())

    return render(request, 'species/browse_species.html', {'data': data})