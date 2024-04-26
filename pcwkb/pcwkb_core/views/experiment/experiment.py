from django.shortcuts import render, get_object_or_404

from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment

def exp_page(request, experiment_name):
    experiment = get_object_or_404(Experiment, experiment_name=experiment_name)

    print (experiment, experiment.experiment_name)

    return render(request, 'relationships/experiment.html', {'experiment':experiment})
