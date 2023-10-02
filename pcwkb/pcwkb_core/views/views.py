from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core import serializers
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    return render(request, 'home.html')

def browse_species(request):

    

    return render(request, 'species/browse_species.html')