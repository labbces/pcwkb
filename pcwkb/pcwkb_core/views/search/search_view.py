from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from haystack.query import SearchQuerySet

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.biomass.cellwall_component import CellWallComponent

def search_engine(request):
    species_list = Species.objects.all().order_by('scientific_name')
    return render(request, 'search/search_results.html', {'species_list': species_list})

def search_pcwkb(request):
    query = request.GET.get('q', '')
    model = request.GET.get('model', 'all')
    species_id = request.GET.get('species_id', 'all')

    search_results = SearchQuerySet().filter(text__exact=query).load_all()

    results = []

    if model == 'species':
        search_results = search_results.models(Species)

        for result in search_results:
            result_data = {}  # Create a new dictionary for each result
            url_species = reverse('species_page', kwargs={'species_code': result.object.species_code})
            result_data['url_species'] = url_species
            result_data['species'] = result.object.scientific_name
            result_data['genes_count'] = Gene.objects.filter(species=result.object).count()
            result_data['cellwallcomp'] = []

            genes = Gene.objects.filter(species=result.object).prefetch_related(
                    'biomassgeneexperimentassoc_set__plant_cell_wall_component'
                    )
            for gene in genes:
                for assoc in gene.biomassgeneexperimentassoc_set.all():
                    result_data['cellwallcomp'].append(assoc.plant_cell_wall_component.cellwallcomp_name)

            result_data['cellwallcomp'] = list(set(result_data['cellwallcomp']))
            results.append(result_data)

    elif model == 'genes':
        search_results = search_results.models(Gene)

        if species_id != 'all':
            species = Species.objects.get(id=species_id)
            search_results = search_results.filter(species=species.scientific_name)

        for result in search_results:
            result_data = {}  # Create a new dictionary for each result
            url_gene = reverse('gene_page', kwargs={'gene_name': result.object.gene_name})
            url_species = reverse('species_page', kwargs={'species_code': result.object.species.species_code })
            result_data['url_gene'] = url_gene
            result_data['url_species'] = url_species
            result_data['gene'] = result.object.gene_name
            result_data['cellwallcomp'] = []
            result_data['species'] = result.object.species.scientific_name

            biomass_gene_assocs = result.object.biomassgeneexperimentassoc_set.all()
            if biomass_gene_assocs.exists():
                for assoc in biomass_gene_assocs:
                    result_data['cellwallcomp'].append(assoc.plant_cell_wall_component.cellwallcomp_name)
            
            result_data['cellwallcomp'] = list(set(result_data['cellwallcomp']))
            results.append(result_data)

    elif model == 'cellwallcomp':
        search_results = search_results.models(CellWallComponent)

        if species_id != 'all':
            species = Species.objects.get(id=species_id)
       
        for result in search_results:
            result_data = {}  # Create a new dictionary for each result
            url_cellwallcomp = reverse('cellwallcomponent_page', kwargs={'cellwallcomp_name': result.object.cellwallcomp_name } )
            result_data['url_cellwallcomp'] = url_cellwallcomp
            result_data['cellwallcomp'] = result.object.cellwallcomp_name
            result_data['species'] = []
            result_data['genes'] = []


            biomass_gene_assocs = result.object.biomassgeneexperimentassoc_set.all()
            if biomass_gene_assocs.exists():
                for assoc in biomass_gene_assocs:
                    if species_id == 'all' or assoc.gene.species.id == species.id:
                        result_data['species'].append(assoc.gene.species.scientific_name)
                        result_data['genes'].append(assoc.gene.gene_name)
                        
            result_data['genes'] = list(set(result_data['genes']))
            result_data['species'] = list(set(result_data['species']))
            
            result_data['cellwallcompquery']=True
            results.append(result_data)

    else:    
        for result in search_results:
            result_data = {}  # Create a new dictionary for each result

            if hasattr(result.object, 'species_code'):
                url_species = reverse('species_page', kwargs={'species_code': result.object.species_code})
                result_data['label'] = query
                result_data['url_species'] = url_species
                result_data['species'] = result.object.scientific_name
                result_data['genes_count'] = Gene.objects.filter(species=result.object).count()
                result_data['cellwallcomp'] = []

                genes = Gene.objects.filter(species=result.object).prefetch_related(
                        'biomassgeneexperimentassoc_set__plant_cell_wall_component'
                        )
                for gene in genes:
                    for assoc in gene.biomassgeneexperimentassoc_set.all():
                        result_data['cellwallcomp'].append(assoc.plant_cell_wall_component.cellwallcomp_name)
    
                result_data['cellwallcomp'] = list(set(result_data['cellwallcomp']))


            elif hasattr(result.object, 'gene_name'):
                url_gene = reverse('gene_page', kwargs={'gene_name': result.object.gene_name})
                url_species = reverse('species_page', kwargs={'species_code': result.object.species.species_code })
                result_data['label'] = query
                result_data['url_gene'] = url_gene
                result_data['url_species'] = url_species
                result_data['species'] = result.object.species.scientific_name
                result_data['gene'] = result.object.gene_name
                result_data['cellwallcomp'] = []

                biomass_gene_assocs = result.object.biomassgeneexperimentassoc_set.all()
                if biomass_gene_assocs.exists():
                    for assoc in biomass_gene_assocs:
                        result_data['cellwallcomp'].append(assoc.plant_cell_wall_component.cellwallcomp_name)
                
                result_data['cellwallcomp'] = list(set(result_data['cellwallcomp']))

            elif hasattr(result.object, 'cellwallcomp_name'):
                url_cellwallcomp = reverse('cellwallcomponent_page', kwargs={'cellwallcomp_name': result.object.cellwallcomp_name } )
                result_data['url_cellwallcomp'] = url_cellwallcomp
                result_data['cellwallcomp'] = result.object.cellwallcomp_name
                result_data['species'] = []
                result_data['genes'] = []
                result_data['cellwallcompquery']=True

                biomass_gene_assocs = result.object.biomassgeneexperimentassoc_set.all()
                if biomass_gene_assocs.exists():
                    for assoc in biomass_gene_assocs:
                        result_data['species'].append(assoc.gene.species.scientific_name)
                        result_data['genes'].append(assoc.gene.gene_name)

                result_data['genes'] = list(set(result_data['genes']))
                result_data['species'] = list(set(result_data['species']))

            results.append(result_data)


    return JsonResponse({'results': results})
