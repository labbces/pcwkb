from django.shortcuts import render
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
    search_results = SearchQuerySet().filter(content_auto__contains=query)

    print(search_results)

    print(query)

    context = {
        'query': query,
        'results': search_results,
    }

    for result in search_results:
        print(result)

    return render(request, 'search/search_results.html', context)  