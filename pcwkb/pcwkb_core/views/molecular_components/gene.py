from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
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

    # Use a set to track unique combinations
    seen = set()
    unique_associations = []
    
    for assoc in data.object_list:
        key = (
            assoc.gene.gene_name,
            assoc.gene.gene_id,
            assoc.plant_cell_wall_component.cellwallcomp_name if assoc.plant_cell_wall_component else None
        )
        if key not in seen:
            seen.add(key)
            unique_associations.append({
                'gene_id': assoc.gene.gene_id,
                'gene_name': assoc.gene.gene_name,
                'chebi': assoc.plant_cell_wall_component.cellwallcomp_name if assoc.plant_cell_wall_component else None,
            })

    print(unique_associations)

    return JsonResponse({
        'data': unique_associations,
        'page': data.number,
        'num_pages': paginator.num_pages
    })


def gene_page(request, gene_name):
    gene = Gene.objects.get(gene_name=gene_name)
    proteins = {}

    proteins_objects = Protein.objects.filter(gene=gene)
    for obj in proteins_objects:
        protein = str(obj.protein_name)
        proteins[protein] = {
            'sequence': obj.sequence,
            'description': obj.description,
            'orthogroup': ProteinOrthogroup.objects.get(protein=obj).orthogroup if ProteinOrthogroup.objects.filter(protein=obj).exists() else None
        }
        print(proteins[protein])

    print(gene.gene_name)

    assoc_objects = BiomassGeneExperimentAssoc.objects.filter(gene=gene)
    associations = list(assoc_objects) if assoc_objects.exists() else None

    context = {
        'gene_id': gene.gene_id,
        'gene_name': gene.gene_name,
        'description': gene.description,
        'original_db_info': gene.original_db_info,
        'proteins': proteins,
        'species': gene.species,
        'assoc_list': associations
    }
    
    print(context)

    return render(request, 'gene/gene_page.html', context)
