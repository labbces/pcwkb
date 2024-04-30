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

def search(request):
    query = request.GET.get('q', '')  # Obtain the search query from the URL parameter

    # Filter search results based on the 'content_auto' field in the indexed model
    scientific_name_results = SearchQuerySet().autocomplete(scientific_name_auto__contains=query)
    common_name_results = SearchQuerySet().autocomplete(common_name_auto__contains=query)

    print(type(scientific_name_results),type(common_name_results))

    search_results = scientific_name_results | common_name_results

    print(search_results)

    print(query)

    context = {
        'query': query,
        'results': search_results,
    }

    for result in search_results:
        print(result)

    return render(request, 'search/search_results.html', context)

def autocomplete(request):
    query = request.GET.get('q', '')
    # Perform autocomplete query
    scientific_name_results = SearchQuerySet().autocomplete(scientific_name_auto=query)[:10]
    common_name_results = SearchQuerySet().autocomplete(common_name_auto=query)[:10]

    # Combine and format the results
    results = []
    for result in scientific_name_results:
        url_species=f"pcwkb_core/species_page/{result.object.species_code}"
        results.append({'label': result.object.scientific_name, 'url': url_species})
    for result in common_name_results:
        url_species=f"pcwkb_core/species_page/{result.object.species_code}"
        results.append({'label': result.object.common_name, 'url': url_species})
    
    print(results)

    return JsonResponse(results, safe=False)