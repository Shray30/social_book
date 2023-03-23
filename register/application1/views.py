from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home_Page(request):
    return render(request, 'home.html')

def sign_Up_Page(request):
    if request.method == 'POST':
        user_Name = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return HttpResponse('Password Mismatch!!')
        else:
            my_User = User.objects.create_user(user_Name, email, password1)
            my_User.save()
            return redirect('login')
    return render(request, 'signup.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_Name = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse('Password Mismatch!!')
        else:
            my_User = User.objects.create_user(user_Name, email, password1)
            my_User.save()
            return redirect('login1')
    return render(request, 'register.html')


def login_Page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            redirect('home')
        else:
            return HttpResponse('Authentication Failed!!')
    return render(request, 'login.html')

def login1_Page(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        print(username, pass1)
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            # return redirect('index_Page')
            context = {
                'username': username
            }
            return render(request, 'index.html', context)
        else:
            return HttpResponse('Authentication Failed!!')
    return render(request, 'login1.html',)

def logout_Page(request):
    logout(request)
    return redirect('login')

def index_Page(request):
    return render(request, 'index.html')


