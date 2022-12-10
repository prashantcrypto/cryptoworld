from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    return render(request, '../templets/authentication/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')

        if password1 != password2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password1)
        myuser.save()

        messages.success(request, 'Account is created Successfully')

        return redirect('signin')

    return render(request, '../templets/authentication/register.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            email = user.email
            print(email)
            return render(request, '../templets/authentication/index.html', {'email': email})

        else:
            messages.error(request, 'Bad Crenditial')
            return redirect('home')

    return render(request, '../templets/authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('home')
