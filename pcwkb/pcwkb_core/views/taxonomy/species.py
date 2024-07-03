from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from django.http import Http404

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.relationships.pcw_genetics_association import BiomassComposition
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc

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
                'photosystem': '',
                'common_name': '',
                'experimental_genes': {},
                'genes_paginated': {},
                'biomass_composition':{},
                'biomass_composition_literature': '',
                }

    context['species_id'] = Species.objects.get(species_code=species_code).id
    context['genes_paginated'] = Gene.objects.filter(species_id=context['species_id'])
    
    species_gene = Gene.objects.filter(species_id=context['species_id'])
    context['genes_biomass_assoc'] = BiomassGeneExperimentAssoc.objects.filter(gene__in=species_gene)

    if BiomassComposition.objects.filter(species_id=context['species_id']).exists():
        BiomassComponent_objects = BiomassComposition.objects.filter(species_id=context['species_id'])
        for obj in BiomassComponent_objects:
            po_name = str(obj.po.po_name)
            context['biomass_composition'][po_name]=obj.components_percentage[0]
            context['biomass_composition_literature']=obj.literature

    context['common_name'] = Species.objects.get(species_code=species_code).common_name
    context['scientific_name'] = Species.objects.get(species_code=species_code).scientific_name
    context['photosystem'] = Species.objects.get(species_code=species_code).photosystem

    name=context['scientific_name'].replace(" ","_")

    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    response = requests.get(wiki_url)
    if response.status_code == 200:
        wikipedia_content = response.json()
    else:
        wikipedia_content = {"extract_html": "We are unable to retrieve the Wikipedia information for this entry at this time. Please try again later."}

    context.update({"wikipedia_content": wikipedia_content})
    
    return render(request, 'species/species_page.html', context)

def browse_species(request):
    """
    Function that shows a cladogram in the browse species page,
    that gets the information from the database and shows in the tree.
    """
    species_data = Species.objects.order_by('scientific_name').values('species_code', 'scientific_name', 'family', 'clade')

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


        """
        Idetifying if species has any experimental data associated based on 
        GeneExperimentAssociation and BiomassGeneExperimentAssoc models
        and adding to the tree
        """
        specie = Species.objects.get(scientific_name=species['scientific_name'])
        species_gene = Gene.objects.filter(species_id=specie)

        genes = Gene.objects.filter(species_id=specie)

        if GeneExperimentAssociation.objects.filter(gene__in=genes) or BiomassGeneExperimentAssoc.objects.filter(gene__in=species_gene):
            family_node["children"].append({"name": f"✓ {species['scientific_name']} ({species['species_code']})"})
        else:
            family_node["children"].append({"name": f"{species['scientific_name']} ({species['species_code']})"})

    data["children"] = list(clade_dict.values())

    return render(request, 'species/browse_species.html', {'data': data})