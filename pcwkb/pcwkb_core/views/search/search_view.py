from django.shortcuts import render
from django.http import JsonResponse
from haystack.query import SearchQuerySet

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene

def search_pcwkb(request):

    print("chegou no search_pcwkb")
    query = request.GET.get('q', '')

    print (query)

    search_results = SearchQuerySet().filter(text=query)

    results={}
    for result in search_results:
        if hasattr(result.object, 'species_code'):
            url_species = f"pcwkb_core/species_page/{result.object.species_code}"
            results['label']=query
            results['url']=url_species

            results['specie']=result.object.scientific_name
            results['genes']=[]
            if Gene.objects.filter(species=result.object):
                for gene in Gene.objects.filter(species=result.object):
                    results['genes'].append(gene.gene_name)

        elif hasattr(result.object, 'gene_name'):
            url_gene = f"pcwkb_core/gene_page/{result.object.gene_name}"
            results['label']=query
            results['url']=url_gene

            results['specie']=result.object.species.scientific_name
            results['genes']=[]
            results['genes'].append(result.object.gene_name)

    print(results)

    return JsonResponse({'results': results})

