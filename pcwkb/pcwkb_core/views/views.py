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

def browse_species(request):

    

    return render(request, 'species/browse_species.html')

def species_page(request):

    context = {'species_name': 'Oriza sativa',
                'common_name': ''}
    context['common_name'] = Species.objects.get(species_name=context['species_name']).common_name
    
    return render(request, 'species/species_page.html', context)