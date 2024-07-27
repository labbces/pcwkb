from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from pcwkb_core.forms.user_forms import CustomUserCreationForm
from django.db import transaction
from pcwkb_core.models.temporary_data.data_submission import DataSubmission
from pcwkb_core.utils.data_submission import replace_nan_with_none
import json

def registration(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Save user to the default database
                user = form.save()

                # Save user to the temporary_data database
                user.save(using='temporary_data')

            login(request, user)  # Log in the user after registration
            messages.success(request, "User registered successfully.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/registration.html', {'form': form})


@login_required
def profile(request):
    # Fetch DataSubmission instances for the logged-in user from the temporary_data database
    data_submissions = DataSubmission.objects.using('temporary_data').filter(user=request.user)
    for submission in data_submissions:
        
        json_data = json.loads(submission.json_data)
        json_data = replace_nan_with_none(json_data)  # Replace NaN with None
        submission.json_data = json.dumps(json_data) 
    
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'data_submissions': data_submissions
    })