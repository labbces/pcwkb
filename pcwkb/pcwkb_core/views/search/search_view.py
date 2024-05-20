from django.shortcuts import render
from django.http import JsonResponse
from haystack.query import SearchQuerySet

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene

def search_pcwkb(request):
    print("Entered search_pcwkb view")
    query = request.GET.get('q', '')

    print(f"Search query: {query}")

    search_results = SearchQuerySet().filter(text=query).load_all()

    results = []
    for result in search_results:
        print(f"Search result: {result}")
        result_data = {}
        if hasattr(result.object, 'species_code'):
            url_species = f"pcwkb_core/species_page/{result.object.species_code}"
            result_data['label'] = query
            result_data['url_species'] = url_species
            result_data['specie'] = result.object.scientific_name
            result_data['genes_count'] = Gene.objects.filter(species=result.object).count()

        elif hasattr(result.object, 'gene_name'):
            url_gene = f"pcwkb_core/gene_page/{result.object.gene_name}"
            url_species = f"pcwkb_core/species_page/{result.object.species.species_code}"
            result_data['label'] = query
            result_data['url_gene'] = url_gene
            result_data['url_species'] = url_species
            result_data['specie'] = result.object.species.scientific_name
            result_data['gene_name'] = result.object.gene_name

        results.append(result_data)

    print(f"Results: {results}")

    return JsonResponse({'results': results})
