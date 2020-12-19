import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from .forms import UserForm, PlantsForm
from .models import Plants, OrderItem, Order, ShippingAddress


@login_required
def home(request):
    if not request.user.is_staff:
        plants = Plants.objects.all()
        return render(request, 'dashboard/customer_dashboard.html', {'plants': plants})
    else:
        return redirect('user:dashboard')

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
            return render(request, 'user/signin.html', {'message': message})

    return render(request, 'user/signin.html')


def index(request):
    return render(request, 'user/signup_index.html')


def signup_type(request, user):
    form = UserForm()
    context = {'form': form}
    if user == 1:
        return render(request, 'user/customer_signup.html', context)
    elif user == 2:
        return render(request, 'user/merchant_signup.html', context)
    else:
        return redirect('user:signup_index')


def signup(request, user):
    global user_form
    registered = False
    if request.method == 'POST':
        # customuser = CustomUser.objects.all()
        # email = request.POST['username']
        # phone = request.POST['phone']
        # password = request.POST['password']

        # for users in customuser:
        #     if email == users.username:
        #         return HttpResponse("Your'e already signed In.")
        # if phone == users.phone:
        #     return HttpResponse("Phone number already registered.")
        if user == 1:
            customer = UserForm(request.POST)
            if customer.is_valid():
                user = customer.save(commit=False)
                user.set_password(request.POST['password'])
                user.save()
                return redirect('user:signin')

        elif user == 2:
            merchant = UserForm(request.POST)
            if merchant.is_valid():
                user = merchant.save(commit=False)
                user.set_password(request.POST['password'])
                user.is_staff = 1
                user.save()
                return redirect('user:signin')
        #
        #     nursery = request.POST['nursery']
        #     mrchnt = CustomUser.objects.get(username=email)
        #     mrchnt.is_staff = True
        #     mrchnt.nursery = nursery
        #     mrchnt.save()
        #     return redirect('user:signin')
        user_form = UserForm(data=request.POST)
    #     if user_form.is_valid():
    #         user = user_form.save()
    #         user.set_password(user.password)
    #         user.save()
    #         registered = True
    #         return redirect('user:signin')
    #     else:
    #         return HttpResponse(user_form.errors)
    # else:
    #     user_form = UserForm()

    return render(request, 'user/signup.html', {'user_form': user_form, 'registered': registered})

@login_required
def dashboard(request):
    print(request.user, request.user.is_staff)
    if request.user.is_authenticated:
        if request.user.is_staff:
            myPlants = Plants.objects.filter(manager=request.user)
            order_items = OrderItem.objects.filter(product_id__in=myPlants.all())

            context = {
                'myplants': myPlants,
                'orders': order_items
            }
            return render(request, 'dashboard/merchant_dashboard.html', context)
        else:
            order = Order.objects.filter(customer=request.user, complete=True)
            order_items = OrderItem.objects.filter(product_id__in=order.all())
            context = {
                'order_items': order_items
            }
            return render(request, 'dashboard/customer_dashboard.html', context)
    else:
        return redirect('user:signin')


@login_required
def signout(request):
    logout(request)
    return redirect('user:signin')


@login_required
def addplant_form(request):
    if request.user.is_staff:
        form = PlantsForm()
        return render(request, 'dashboard/add_plants.html', {'form': form})


@login_required
def addplant(request):
    if request.user.is_staff and request.method == 'POST':
        plant = PlantsForm(request.POST, request.FILES)
        if plant.is_valid:
            p = plant.save(commit=False)
            p.manager = request.user
            plant.save()
            return HttpResponseRedirect(reverse("nurseryapp:dashboard"))
    else:
        return HttpResponse("Waait a min, Who Are You ?")


@login_required(login_url='nurseryapp:login_page')
def cart_action(request, p_id, action):
    user = request.user
    product = Plants.objects.get(id=p_id)
    order, created = Order.objects.get_or_create(customer=user, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 1:  # for add item
        orderitem.quantity += 1
    elif action == 0:  # For Remove Item
        orderitem.quantity -= 1

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return HttpResponseRedirect(reverse('user:cart'))


@login_required
def cart(request):
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    return render(request, 'dashboard/cart.html', {'items': items, 'order': order})


@login_required
def checkout(request):
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    return render(request, 'dashboard/checkout.html', {'items': items, 'order': order})


@login_required(login_url='user:login')
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()

    customer = request.user

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    total = order.get_cart_total
    order.transaction_id = transaction_id

    order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=request.POST['address'],
        city=request.POST['city'],
        state=request.POST['state'],
        pincode=request.POST['pincode'],
    )

    return HttpResponseRedirect(reverse('user:dashboard'))
