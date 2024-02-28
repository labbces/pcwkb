from django.shortcuts import render

def results(request):
    return render(request, 'search_results.html')