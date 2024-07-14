from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from pcwkb_core.forms.data_submission.data_submission import DataSubmissionForm, ExperimentForm
from pcwkb_core.models.temporary_data.data_submission import DataSubmission

'''def index(request):
    return render(request, 'forms/data_submission.html')
'''
"""
def get_data_file(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = DataSubmissionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DataSubmissionForm()
    
    return render(request, "forms/data_submission.html", {"form": form})
"""

def data_submission_view(request):
    if request.method == 'POST':
        form = DataSubmissionForm(request.POST, request.FILES,)
        if form.is_valid():
            json_data = form.process_file() 
            DataSubmission.objects.create(
                title=form.cleaned_data['title'],
                json_data=json_data
            )
            messages.success(request, 'Data submitted successfully!')
            return redirect('data_submission')
    else:
        form = DataSubmissionForm()
    
    return render(request, 'forms/data_submission.html', {'form': form})


def experiment_form_view(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                instance.save(using='temporary_data')
                messages.success(request, 'Experiment form submitted successfully.')
                return redirect('/pcwkb_core/')
            except Exception as e:
                messages.error(request, f'Error saving form: {str(e)}')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = ExperimentForm()

    return render(request, 'forms/experiment_form.html', {'form': form})