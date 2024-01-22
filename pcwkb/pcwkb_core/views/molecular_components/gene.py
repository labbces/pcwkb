from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import JsonResponse

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation


def paginated_gene_list(request, species_id):
    page_number = request.GET.get('page', 1)
    data_list = Gene.objects.filter(species_id=species_id)
    paginator = Paginator(data_list, 3)

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



def gene_page(request, gene_id):
    
    gene = Gene.objects.get(id=gene_id)

    context = {'gene_id': gene_id,
               'gene_name': gene.gene_name,
               'description': gene.description}
    
    return render(request, 'gene/gene_page.html', context)