from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.signin, name='signin'),

    path('index/', views.index, name='index'),
    path('signup/<int:user>/', views.signup_type, name='signup_type'),
    path('signup/post/<int:user>/', views.signup, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.signout, name='logout'),

    path('addplant_form/', views.addplant_form, name='addplant_form'),
    path('addplant/', views.addplant, name='addplant'),

    path('cart_action/<int:p_id>/<int:action>/', views.cart_action, name="cart_action"),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.process_order, name='process_order'),
]
