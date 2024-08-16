from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from pcwkb_core.forms.data_submission.data_submission import DataSubmissionForm, ExperimentForm
from pcwkb_core.models.temporary_data.data_submission import DataSubmission
from django.contrib.auth.decorators import login_required
import json
from django.db import transaction, DatabaseError
from rolepermissions.decorators import has_permission_decorator

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

@login_required
@has_permission_decorator('submit_data')
def data_submission_view(request):
    if request.method == 'POST':
        form = DataSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.process_file()
            # Validate data
            errors, warnings = form.validate_data(data)

            # Handle warnings
            if warnings:
                for field, field_warnings in warnings.items():
                    for field_name, warnings_list in field_warnings.items():
                        messages_list=[]
                        for warnings in warnings_list:
                            messages_list.append(warnings)
                        messages_list="<br>".join(messages_list)
                        messages.warning(request, mark_safe(f"Validation warnings in <b>{field}</b> sheet <b>{field_name} column</b>:<br>{messages_list}"))

            # Handle errors
            invalid_species_error = False
            if errors:
                for field, field_errors in errors.items():
                    # Check for specific error message
                    if "experiment_species" in field_errors:
                        invalid_species_error = True

                    for field_name, error_list in field_errors.items():
                        messages_list=[]
                        for error in error_list:
                            messages_list.append(error)
                        messages_list="<br>".join(messages_list)
                        messages.error(request, mark_safe(f"Validation errors in <b>{field}</b> sheet <b>{field_name} column</b>:<br><b>{messages_list}</b>"))
                
                if invalid_species_error:
                    messages.error(request, "Invalid reference for species. Please complete the species_data sheet or submit a new species using the form.")
                    return render(request, 'forms/data_submission.html', {'form': form, 'invalid_species_error': True})

                return render(request, 'forms/data_submission.html', {'form': form})

            # Save valid data if there are no errors
            try:
                with transaction.atomic():
                    DataSubmission.objects.using('temporary_data').create(
                        title=form.cleaned_data['title'],
                        json_data=json.dumps(data),
                        data_type=form.cleaned_data['type_of_data'],
                        user=request.user,
                        reviewed=False
                    )
                messages.success(request, f"Data submitted successfully by {request.user}!")
                return redirect('data_submission')
            except DatabaseError as e:
                messages.error(request, f"An error occurred while saving the data submission. Please try again. {e}")
                return render(request, 'forms/data_submission.html', {'form': form})
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

@login_required
def approve_submission_DataSubmission(request, submission_id):
    if not has_role(request.user, 'reviewer'):
        return redirect('profile')  # Or return an error response

    submission = get_object_or_404(DataSubmission, id=submission_id, reviewed=False)
    submission.reviewed = True
    submission.save(using='temporary_data')

    return redirect('profile')