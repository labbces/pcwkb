from django.shortcuts import render
from django.http import JsonResponse
from haystack.query import SearchQuerySet

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.biomass.cellwall_component import CellWallComponent

def search_engine(request):
    species_list = Species.objects.all()
    return render(request, 'search/search_results.html', {'species_list': species_list})

def search_pcwkb(request):
    query = request.GET.get('q', '')
    model = request.GET.get('model', 'all')
    species_id = request.GET.get('species_id', 'all')

    search_results = SearchQuerySet().filter(content__exact=query).load_all()
    results = []
    result_data = {}

    if model == 'species':
        search_results = search_results.models(Species)

        for result in search_results:
            if hasattr(result.object, 'species_code'):
                url_species = f"pcwkb_core/species_page/{result.object.species_code}"
                result_data['label'] = query
                result_data['url_species'] = url_species
                result_data['specie'] = result.object.scientific_name
                result_data['genes_count'] = Gene.objects.filter(species=result.object).count()
            results.append(result_data)


    elif model == 'genes':
        search_results = search_results.models(Gene)

        if species_id != 'all':
            species = Species.objects.get(id=species_id)
            search_results = search_results.filter(species=species.scientific_name)

        count=1

        for result in search_results:
            if hasattr(result.object, 'gene_name'):
                url_gene = f"pcwkb_core/gene_page/{result.object.gene_name}"
                url_species = f"pcwkb_core/species_page/{result.object.species.species_code}"
                result_data['label'] = query
                result_data['url_gene'] = url_gene
                result_data['url_species'] = url_species
                result_data['specie'] = result.object.species.scientific_name
                result_data['gene_name'] = result.object.gene_name
            results.append(result_data)
    
    elif model == 'cellwallcomp':
        search_results = search_results.models(CellWallComponent)
        if species_id != 'all':
            species = Species.objects.get(id=species_id)
            search_results = search_results.filter(species=species.scientific_name)
    
    else:    
        for result in search_results:
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
    
    print(results)

    return JsonResponse({'results': results})
