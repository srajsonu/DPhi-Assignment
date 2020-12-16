from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from user.forms import UserForm


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active():
                login(request, user)
                return redirect('user:dashboard')
            else:
                return HttpResponse('Your account is not active')
        else:
            return render(request, 'signin.html')

    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect('user:signin')
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'signup.html', {'user_form': user_form})

def dashboard(request):
    return render(request, 'base.html')

@login_required
def logout(request):
    logout()
    return redirect('user:signin')
