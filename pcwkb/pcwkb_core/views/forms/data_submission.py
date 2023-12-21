from django.shortcuts import render
from django.http import HttpResponseRedirect
from pcwkb_core.forms.data_submission.data_submission import DataSubmissionForm

def index(request):
    return render(request, 'forms/data_submission.html')

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
            return HttpResponseRedirect("")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DataSubmissionForm()

    return render(request, "forms/data_submission.html", {"form": form})