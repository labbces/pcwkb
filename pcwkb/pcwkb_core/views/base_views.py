from django.shortcuts import render

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
    query = request.GET.get('q', '')  # Obtém a consulta de pesquisa do usuário da URL

    if query:
        search_results = SearchQuerySet().filter(content_auto__contains=query)
    else:
        search_results = []

    context = {
        'query': query,
        'results': search_results,
    }

    return render(request, 'search_results.html', context)