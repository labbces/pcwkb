from django.shortcuts import render
from django.http import JsonResponse
from haystack.query import SearchQuerySet

def index(request):
    return render(request, 'home.html')

def faq(request):
    return render(request, 'faq.html')

def team(request):
    return render(request, 'team.html')

def funding(request):
    return render(request, 'funding.html')

def ontologies(request):
    return render(request, 'ontologies.html')

def search_engine(request):
    return render(request, 'search/search_results.html')


def search_pcwkb(request):

    print("chegou no search_pcwkb")
    query = request.GET.get('q', '')

    print (query)

    search_results = SearchQuerySet().filter(text=query)

    results={}
    for result in search_results:
        url_species=f"pcwkb_core/species_page/{result.object.species_code}"
        results['label']=result.object.scientific_name
        results['url']=url_species

    print(results)

    return JsonResponse({'results': results})

def autocomplete(request):
    query = request.GET.get('q', '')
    # Perform autocomplete query
    scientific_name_results = SearchQuerySet().autocomplete(scientific_name_auto__contains=query)[:10]
    common_name_results = SearchQuerySet().autocomplete(common_name_auto__contains=query)[:10]

    # Combine and format the results
    results = []
    for result in scientific_name_results:
        url_species=f"pcwkb_core/species_page/{result.object.species_code}"
        results.append({'label': result.object.scientific_name})
    for result in common_name_results:
        url_species=f"pcwkb_core/species_page/{result.object.species_code}"
        results.append({'label': result.object.common_name})
    
    print(results)

    return JsonResponse(results, safe=False)