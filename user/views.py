from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .forms import UserForm

def dashboard(request):
    return render(request, 'dashboard.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        message = 'User is ' + str(user)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('user:dashboard')
            else:
                return HttpResponse('Your account is not active')
        else:
            return render(request, 'signin.html', {'message': message})

    return render(request, 'signin.html')

def index(request):
    return render(request, 'index.html')

def signup_type(request, user):
    form = UserForm()
    context = {'form': form}
    if user == 1:
        return render(request, 'customer_signup.html', context)
    elif user == 2:
        return render(request, 'merchant_signup.html', context)
    else:
        return redirect('user:index')

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            return redirect('user:signin')
        else:
            return HttpResponse(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'signup.html', {'user_form': user_form})


@login_required
def signout(request):
    logout(request)
    return redirect('user:signin')

