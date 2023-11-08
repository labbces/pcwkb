from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core import serializers
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species


def index(request):
    return render(request, 'home.html')

def faq(request):
    return render(request, 'faq.html')

def team(request):
    return render(request, 'team.html')

def funding(request):
    return render(request, 'funding.html')

def browse_species(request):
    return render(request, 'species/browse_species.html')

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

def species_page(request, species_code):

    context = { 'species_code': species_code,
                'scientific_name': '',
                'common_name': ''}

    context['common_name'] = Species.objects.get(species_code=species_code).common_name
    context['scientific_name'] = Species.objects.get(species_code=species_code).scientific_name
    
    return render(request, 'species/species_page.html', context)