from django.shortcuts import render

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation

def species_page(request, species_code):

    context = { 'species_code': species_code,
                'species_id': '',
                'scientific_name': '',
                'common_name': '',
                'experimental_genes': {}}

    context['species_id'] = Species.objects.get(species_code=species_code).id
    context['experimental_genes'] = GeneExperimentAssociation.objects.filter(species_id=context['species_id'])

    context['common_name'] = Species.objects.get(species_code=species_code).common_name
    context['scientific_name'] = Species.objects.get(species_code=species_code).scientific_name
    
    return render(request, 'species/species_page.html', context)

def browse_species(request):
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