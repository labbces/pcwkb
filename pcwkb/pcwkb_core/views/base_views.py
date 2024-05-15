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

def autocomplete(request):
    query = request.GET.get('q', '')
    # Perform autocomplete query
    scientific_name_results = SearchQuerySet().autocomplete(scientific_name_auto__contains=query)[:10]
    common_name_results = SearchQuerySet().autocomplete(common_name_auto__contains=query)[:10]
    gene_name_results = SearchQuerySet().autocomplete(gene_name_auto__contains=query)[:10]
    gene_description_results = SearchQuerySet().autocomplete(gene_description_auto__contains=query)[:10]

    # Combine and format the results
    results = []
    for result in scientific_name_results:
        results.append({'label': result.object.scientific_name})
    for result in common_name_results:
        results.append({'label': result.object.common_name})
    for result in gene_name_results:
        results.append({'label': result.object.gene_name})
    for result in gene_description_results:
        results.append({'label': result.object.description})
    
    print(results)

    return JsonResponse(results, safe=False)