from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation
from pcwkb_core.models.molecular_components.relationships.pcw_genetics_association import BiomassComposition

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
                'biomass_composition':{}
                }

    context['species_id'] = Species.objects.get(species_code=species_code).id
    context['genes_paginated'] = Gene.objects.filter(species_id=context['species_id'])

    if BiomassComposition.objects.filter(species_id=context['species_id']).exists():
        BiomassComponent_objects = BiomassComposition.objects.filter(species_id=context['species_id'])
        for obj in BiomassComponent_objects:
            po_name = str(obj.po).split(":")[-1].strip()
            context['biomass_composition'][po_name]=obj.components_percentage[0]

    context['common_name'] = Species.objects.get(species_code=species_code).common_name
    context['scientific_name'] = Species.objects.get(species_code=species_code).scientific_name

    print(context)
    
    return render(request, 'species/species_page.html', context)

def browse_species(request):
    """
    Function that shows a cladogram in the browse species page,
    that gets the information from the database and shows in the tree.
    """
    species_data = Species.objects.values('species_code', 'scientific_name', 'common_name', 'family', 'clade', 'photosystem')
    print(species_data)

    data = {"name": "Angiospermae", "children": []}

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