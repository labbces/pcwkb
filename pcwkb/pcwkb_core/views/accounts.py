from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from pcwkb_core.forms.user_forms import CustomUserCreationForm
from django.db import transaction
from pcwkb_core.models.temporary_data.data_submission import DataSubmission
from pcwkb_core.models.correctingmessages import CorrectionMessage

from rolepermissions.checkers import has_role
from rolepermissions.decorators import has_role_decorator

from pcwkb_core.utils.data_submission import create_biomass_gene_experiment_assoc, get_or_create_species, get_or_create_experiment, create_gene_gene_interation
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
@has_role_decorator('reviewer')
def handle_review_action(request, submission_id):
    submission = DataSubmission.objects.using('temporary_data').get(id=submission_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        message_content = request.POST.get('reviewer_message', '')

        if action == 'approve':
            submission.clean_json_data()
            data = json.loads(submission.json_data)
            
            if submission.data_type == 'biomass_gene_association_data':
                create_biomass_gene_experiment_assoc(data)

            elif submission.data_type == 'species_data':
                for record in data['species_data']:
                    get_or_create_species(record)

            elif submission.data_type == 'experiment_data':
                for record in data['experiment_data']:
                    get_or_create_experiment(record)
            
            elif submission.data_type == 'gene_gene_association_data':
                create_gene_gene_interation(data)

            submission.reviewed = True
            submission.save(using='temporary_data')

            messages.success(request, 'Submission approved successfully.')

        elif action == 'request_correction':
            # Debugging information
            print(f"Request user database: {request.user._state.db}")
            print(f"Submission user: {submission.user._state.db}")

            User = get_user_model()
            reviewer = User.objects.using('default').get(pk=request.user.pk)
            user = User.objects.using('default').get(pk=submission.user.pk) # Ensure the user is from the default database

            # Debugging information
            print(f"Reviewer database: {reviewer._state.db}")

            CorrectionMessage.objects.using('default').create(
                user=user,
                title=f"Correction Request for {submission.title}",
                content=message_content,
                reviewer=reviewer
            )

            submission.reviewed = False
            submission.save(using='temporary_data')
            messages.success(request, 'Correction requested and message saved.')

    return redirect('users-profile')


@login_required
def profile(request):
    is_collaborator = has_role(request.user, 'collaborator')
    is_reviewer = has_role(request.user, 'reviewer')

    data_submissions = DataSubmission.objects.using('temporary_data').filter(user=request.user)
    for submission in data_submissions:
        submission.clean_json_data()
    
    review_submissions = DataSubmission.objects.using('temporary_data').filter(reviewed=False)
    for submission in review_submissions:
        submission.clean_json_data()

    user_messages = CorrectionMessage.objects.filter(user=request.user)


    return render(request, 'registration/profile.html', {
        'user': request.user,
        'user_messages': user_messages,
        'data_submissions': data_submissions,
        'review_submissions': review_submissions if is_reviewer else None,
        'is_collaborator': is_collaborator,
        'is_reviewer': is_reviewer,
    })