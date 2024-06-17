from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import JsonResponse

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
from pcwkb_core.models.molecular_components.relationships.protein_orthogroup import ProteinOrthogroup
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc


def paginated_gene_list(request, species_id):
    page_number = request.GET.get('page', 1)
    data_list = Gene.objects.filter(species_id=species_id)
    paginator = Paginator(data_list, 15)

    try:
        data = paginator.page(page_number)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serialized_data = list(data.object_list.values())

    print(serialized_data)

    return JsonResponse({
        'data': serialized_data,
        'page': data.number,
        'num_pages': paginator.num_pages
    })

def paginated_gene_experiment_list(request, species_id):
    species_gene = Gene.objects.filter(species_id=species_id)

    page_number = request.GET.get('page', 1)
    data_list = BiomassGeneExperimentAssoc.objects.filter(gene__in=species_gene)
    paginator = Paginator(data_list, 15)

    try:
        data = paginator.page(page_number)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serialized_data = list(data.object_list.values())

    assoc_objects = BiomassGeneExperimentAssoc.objects.filter(gene__in=species_gene)

    if assoc_objects:
        associations = []
        for assoc in assoc_objects:
            associations.append({
                'gene_id': assoc.gene.gene_id,
                'gene_name': assoc.gene.gene_name,
                'chebi': assoc.chebi.chebi_name if assoc.chebi else None,
                'effect_on_plant_cell_wall_component': assoc.effect_on_plant_cell_wall_component,
            })
    
    else:
        associations = None
    print(serialized_data)
    print(associations)

    return JsonResponse({
        'data': associations,
        'page': data.number,
        'num_pages': paginator.num_pages
    })


def gene_page(request, gene_name):

    print(gene_name)

    gene = Gene.objects.get(gene_name=gene_name)

    proteins = {}

    proteins_objects = Protein.objects.filter(gene=gene)
    if proteins_objects:
        for obj in proteins_objects:
            protein = str(obj.protein_name)
            proteins[protein] = {}
            proteins[protein]['sequence'] = obj.sequence
            proteins[protein]['description'] = obj.description
            if ProteinOrthogroup.objects.filter(protein=obj):
                og = ProteinOrthogroup.objects.get(protein=obj).orthogroup
                proteins[protein]['orthogroup'] = og
            print(proteins[protein])

    print(gene.gene_name)

    assoc_objects = BiomassGeneExperimentAssoc.objects.filter(gene=gene)

    if assoc_objects:
        associations = []
        for assoc in assoc_objects:
            associations.append(assoc)
            experiment_names = [experiment.experiment_name for experiment in assoc.experiment.all()]
            print("Experiment Names:", experiment_names)

        context = {'gene_id': gene.gene_id,
                'gene_name': gene.gene_name,
                'description': gene.description,
                'source': gene.source,
                'proteins': proteins,
                'species':gene.species,
                'assoc_list': associations}
    else:
        context = {'gene_id': gene.gene_id,
                'gene_name': gene.gene_name,
                'description': gene.description,
                'source': gene.source,
                'proteins': proteins,
                'species':gene.species,
                'assoc_list': None}
    
    print(context)

    return render(request, 'gene/gene_page.html', context)
