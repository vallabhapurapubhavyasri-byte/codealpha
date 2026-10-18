from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Order, OrderItem

# --- PHASE 4: CATALOG & HOME VIEWS ---

def home(request):
    """
    Renders the StyleCart home page with the top 4 latest products from SQLite.
    """
    featured_products = Product.objects.all().order_by('-created_at')[:4]
    context = {
        'products': featured_products,
    }
    return render(request, 'home.html', context)

def products(request):
    """
    Renders the catalog of products, supporting search and category filtering.
    """
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()

    products_list = Product.objects.all().order_by('-created_at')

    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if category_filter:
        products_list = products_list.filter(category__iexact=category_filter)

    categories = [choice[0] for choice in Product.CATEGORY_CHOICES]

    context = {
        'products': products_list,
        'search_query': search_query,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'products.html', context)

# --- PHASE 5: PRODUCT DETAIL VIEW ---

def product_detail_preview(request):
    """Fallback preview view."""
    return render(request, 'product_detail.html')

def product_detail(request, product_id):
    """
    Renders details for a specific product, along with related products from the same category.
    """
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)

# --- PHASE 6: USER AUTHENTICATION (Register, Login, Logout) ---

def register_view(request):
    """
    Handles user registration:
    - Validates matching passwords and minimum length.
    - Checks that username and email are not already registered.
    - Automatically signs the user in upon successful registration.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Input validation
        if not username or not password:
            messages.error(request, "Username and password cannot be empty.")
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'register.html')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"The username '{username}' is already taken.")
            return render(request, 'register.html')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email address already exists.")
            return render(request, 'register.html')

        # Create user using Django's secure create_user helper (hashes the password)
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f"Welcome to StyleCart, {username}! Your account was created successfully.")
        return redirect('home')

    return render(request, 'register.html')

def login_view(request):
    """
    Handles user login:
    - Authenticates username and password credentials.
    - Creates user session upon valid credentials.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'login.html')

def logout_view(request):
    """
    Logs out the user and destroys their session.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully. Come back soon!")
    return redirect('home')

# --- PHASE 7: SHOPPING CART (Session-based) ---

def cart(request):
    """
    Renders the shopping cart page with all added products,
    item subtotals, and overall order total calculated dynamically.
    """
    # Retrieve cart dictionary from session (format: {product_id_str: quantity_int})
    session_cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id_str, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            # If a product was deleted from DB while in cart, safely skip it
            continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    """
    Adds a specified quantity of a product to the user's session cart.
    """
    product = get_object_or_404(Product, id=product_id)
    session_cart = request.session.get('cart', {})
    product_key = str(product_id)

    # Get quantity from the POST form (default to 1)
    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

    # Check available stock
    current_in_cart = session_cart.get(product_key, 0)
    if current_in_cart + quantity > product.stock:
        quantity_to_add = max(0, product.stock - current_in_cart)
        if quantity_to_add == 0:
            messages.warning(request, f"Cannot add more '{product.name}'. Maximum stock reached ({product.stock} available).")
            return redirect('cart')
        else:
            session_cart[product_key] = product.stock
            messages.warning(request, f"Added {quantity_to_add} '{product.name}' (limited to available stock).")
    else:
        session_cart[product_key] = current_in_cart + quantity
        messages.success(request, f"Added {quantity}x '{product.name}' to your cart!")

    # Save the updated cart dictionary back into session
    request.session['cart'] = session_cart
    request.session.modified = True

    return redirect('cart')

def increase_quantity(request, product_id):
    """
    Increases the quantity of a product in the cart by 1.
    """
    product = get_object_or_404(Product, id=product_id)
    session_cart = request.session.get('cart', {})
    product_key = str(product_id)

    if product_key in session_cart:
        if session_cart[product_key] < product.stock:
            session_cart[product_key] += 1
            request.session['cart'] = session_cart
            request.session.modified = True
        else:
            messages.warning(request, f"Only {product.stock} units of '{product.name}' available in stock.")

    return redirect('cart')

def decrease_quantity(request, product_id):
    """
    Decreases the quantity of a product in the cart by 1.
    If quantity drops to 0, removes it from the cart.
    """
    session_cart = request.session.get('cart', {})
    product_key = str(product_id)

    if product_key in session_cart:
        session_cart[product_key] -= 1
        if session_cart[product_key] <= 0:
            del session_cart[product_key]
        request.session['cart'] = session_cart
        request.session.modified = True

    return redirect('cart')

def remove_from_cart(request, product_id):
    """
    Completely removes a product from the shopping cart.
    """
    product = get_object_or_404(Product, id=product_id)
    session_cart = request.session.get('cart', {})
    product_key = str(product_id)

    if product_key in session_cart:
        del session_cart[product_key]
        request.session['cart'] = session_cart
        request.session.modified = True
        messages.info(request, f"Removed '{product.name}' from your cart.")

    return redirect('cart')

# --- PHASE 8: CHECKOUT & ORDER PROCESSING ---

def checkout(request):
    """
    Renders the checkout shipping details and order review page.
    Redirects to products if the cart is empty.
    """
    session_cart = request.session.get('cart', {})
    if not session_cart:
        messages.warning(request, "Your shopping cart is currently empty. Add products before checking out.")
        return redirect('products')

    cart_items = []
    total_price = 0

    for product_id_str, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    if not cart_items:
        messages.warning(request, "No valid items found in cart.")
        return redirect('products')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)

def process_order(request):
    """
    Handles checkout form submission:
    - Validates shipping and contact details.
    - Creates the Order record in SQLite.
    - Creates OrderItem records for each item in the cart.
    - Reduces product stock inventory.
    - Clears the session cart upon success.
    - Redirects to the order confirmation receipt page.
    """
    if request.method != 'POST':
        return redirect('checkout')

    session_cart = request.session.get('cart', {})
    if not session_cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('products')

    # Collect form inputs
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    zip_code = request.POST.get('zip_code', '').strip()
    payment_method = request.POST.get('payment_method', 'COD').strip()

    # Form validation
    if not (full_name and email and phone and address and city and state and zip_code):
        messages.error(request, "Please fill in all required shipping address fields.")
        return redirect('checkout')

    # Retrieve products and verify stock availability
    order_items_data = []
    total_price = 0

    for product_id_str, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            if quantity > product.stock:
                messages.error(request, f"Sorry, only {product.stock} units of '{product.name}' are available right now.")
                return redirect('cart')
            subtotal = product.price * quantity
            total_price += subtotal
            order_items_data.append((product, quantity, subtotal))
        except Product.DoesNotExist:
            continue

    if not order_items_data:
        messages.error(request, "Your cart contains invalid products.")
        return redirect('cart')

    # Create the Order record in database
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        total_price=total_price,
        payment_method=payment_method,
        status='Pending'
    )

    # Create individual OrderItem records and decrement product stock
    for product, quantity, subtotal in order_items_data:
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=quantity
        )
        # Deduct purchased quantity from store stock
        product.stock -= quantity
        product.save()

    # Empty user's cart
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, f"Congratulations! Your order #STYLE-{order.id} has been placed successfully.")
    return redirect('order_success', order_id=order.id)

def order_success(request, order_id):
    """
    Renders the order confirmation receipt page.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})

