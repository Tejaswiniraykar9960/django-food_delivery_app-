from django import forms
from .models import MenuItem, Order, Restaurant
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price', 'is_available']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
