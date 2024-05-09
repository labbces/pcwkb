from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import JsonResponse

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
from pcwkb_core.models.molecular_components.relationships.protein_orthogroup import ProteinOrthogroup
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation


def paginated_gene_list(request, species_id):
    page_number = request.GET.get('page', 1)
    data_list = Gene.objects.filter(species_id=species_id)
    paginator = Paginator(data_list, 500)

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


def gene_page(request, gene_name):

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

    context = {'gene_id': gene.id,
               'gene_name': gene,
               'description': gene.description,
               'proteins': proteins,
               'species':gene.species}
    print(context)

    return render(request, 'gene/gene_page.html', context)
