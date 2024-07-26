from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from pcwkb_core.forms.user_forms import CustomUserCreationForm
from django.db import transaction

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
    return render (request, 'registration/profile.html')