from django.shortcuts import render, get_object_or_404

from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment

def experiment(request):

    context={"experiments":{}}

    for experiment in Experiment.objects.all():
        experiment_name = experiment.experiment_name
        context["experiments"][experiment_name] = {
            "description": experiment.description,
            "eco": experiment.eco_term
        }

    return render(request, 'experiments.html',  context)

def exp_page(request, experiment_name):
    context = {}
    
    experiment = get_object_or_404(Experiment, experiment_name=experiment_name)

    biomass_gene_assocs = experiment.biomassgeneexperimentassoc_set.all()

    if biomass_gene_assocs.exists():
        assoc_list = {}
        assoc_list['species']=[]
        assoc_list['genes']=[]

        for assoc in biomass_gene_assocs:
            assoc_list['species'].append(assoc.gene.species)
            assoc_list['genes'].append(assoc.gene)

        assoc_list['genes_count']=len(assoc_list['genes'])
        assoc_list['apecies_count']=len(assoc_list['species'])

        print(assoc_list['species'])


        context = {
            "experiment": experiment,
            "assoc_list": assoc_list,  
        }

    else:
        context = {
            "experiment": experiment,
            "assoc_list": None, 
        }

    return render(request, 'relationships/experiment.html', context)
