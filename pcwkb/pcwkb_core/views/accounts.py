from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User

def registration(request):
    if request.method=="GET":
        return render (request, 'registration/registration.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username).first()

        if user:
           return HttpResponse("Username already exists")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return HttpResponse("User register succeeded: "+username)