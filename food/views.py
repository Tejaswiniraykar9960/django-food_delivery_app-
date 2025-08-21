from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from .models import Restaurant, MenuItem, Order, OrderItem
from .forms import MenuItemForm, CheckoutForm, RegisterForm, RestaurantForm

# Home page - List all restaurants
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'food/home.html', {'restaurants': restaurants})

# Restaurant menu page
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = restaurant.menu_items.filter(is_available=True)
    return render(request, 'food/restaurant_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})

# User registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Create restaurant profile
@login_required
def create_restaurant_profile(request):
    if hasattr(request.user, 'restaurant_profile'):
        return redirect('restaurant_dashboard')
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect('restaurant_dashboard')
    else:
        form = RestaurantForm()
    return render(request, 'food/create_restaurant.html', {'form': form})

# Restaurant dashboard
@login_required
def restaurant_dashboard(request):
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    menu_items = restaurant.menu_items.all()
    orders = restaurant.orders.order_by('-created_at')
    return render(request, 'food/restaurant_dashboard.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'orders': orders
    })

# Add menu item
@login_required
def menu_item_create(request):
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect('restaurant_dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'food/menu_item_form.html', {'form': form})

# Edit menu item
@login_required
def menu_item_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    menu_item = get_object_or_404(MenuItem, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('restaurant_dashboard')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'food/menu_item_form.html', {'form': form})

# --- CART FUNCTIONS ---
def _get_cart(request):
    return request.session.get('cart', {})

def add_to_cart(request, item_id):
    cart = _get_cart(request)
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0.00')
    for item_id, qty in cart.items():
        menu_item = get_object_or_404(MenuItem, pk=int(item_id))
        subtotal = menu_item.price * qty
        items.append({'menu_item': menu_item, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'food/cart.html', {'items': items, 'total': total})

def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    return redirect('cart')

# Checkout
@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('home')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            menu_items = MenuItem.objects.filter(id__in=map(int, cart.keys()))
            restaurant = menu_items[0].restaurant
            order = Order.objects.create(
                user=request.user,
                restaurant=restaurant,
                address=form.cleaned_data['address']
            )
            total = Decimal('0.00')
            for menu_item in menu_items:
                qty = cart[str(menu_item.id)]
                subtotal = menu_item.price * qty
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=qty,
                    price=menu_item.price
                )
                total += subtotal
            order.total_price = total
            order.save()
            request.session['cart'] = {}
            return redirect('order_detail', pk=order.pk)
    else:
        form = CheckoutForm()
    items = []
    total = Decimal('0.00')
    for item_id, qty in cart.items():
        menu_item = get_object_or_404(MenuItem, pk=int(item_id))
        subtotal = menu_item.price * qty
        items.append({'menu_item': menu_item, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'food/checkout.html', {'form': form, 'items': items, 'total': total})

# Orders
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user and getattr(request.user, 'restaurant_profile', None) != order.restaurant:
        return redirect('home')
    return render(request, 'food/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    orders = request.user.orders.order_by('-created_at')
    return render(request, 'food/order_list.html', {'orders': orders})

# Simple API endpoint for menu items
def api_menu_items(request, restaurant_id):
    items = MenuItem.objects.filter(restaurant_id=restaurant_id, is_available=True)
    data = [{'id': i.id, 'name': i.name, 'price': str(i.price)} for i in items]
    return JsonResponse({'menu_items': data})

