from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Product, Order, OrderItem

class StyleCartComprehensiveTests(TestCase):
    """
    Comprehensive automated test suite verifying all 18 required features
    of the StyleCart e-commerce application.
    """

    def setUp(self):
        self.client = Client()

        # Create sample products
        self.p1 = Product.objects.create(
            name='Test Cotton Shirt',
            category='Apparel',
            price=Decimal('25.00'),
            description='Breathable cotton shirt for testing.',
            stock=10
        )
        self.p2 = Product.objects.create(
            name='Test Sports Shoes',
            category='Footwear',
            price=Decimal('80.00'),
            description='Running shoes for fitness and training.',
            stock=5
        )

        # Create a test regular user
        self.user = User.objects.create_user(
            username='shopper1',
            email='shopper1@example.com',
            password='testpassword123'
        )

        # Create a test superuser for admin testing
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123'
        )

    # 1. Product Model Tests
    def test_product_model(self):
        self.assertEqual(str(self.p1), 'Test Cotton Shirt - $25.00')
        self.assertEqual(self.p1.stock, 10)
        self.assertEqual(self.p1.price, Decimal('25.00'))

    # 2. Page Navigation & HTTP Status Tests
    def test_page_status_codes(self):
        urls = [
            reverse('home'),
            reverse('products'),
            reverse('product_detail', args=[self.p1.id]),
            reverse('cart'),
            reverse('login'),
            reverse('register'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed for {url}")

    # 3. Product Search and Category Filtering
    def test_product_search_and_filter(self):
        # Search for "Shirt"
        response_search = self.client.get(reverse('products') + '?q=Shirt')
        self.assertContains(response_search, 'Test Cotton Shirt')
        self.assertNotContains(response_search, 'Test Sports Shoes')

        # Filter by Footwear
        response_cat = self.client.get(reverse('products') + '?category=Footwear')
        self.assertContains(response_cat, 'Test Sports Shoes')
        self.assertNotContains(response_cat, 'Test Cotton Shirt')

    # 4. Product Details Page
    def test_product_detail_page(self):
        response = self.client.get(reverse('product_detail', args=[self.p1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Cotton Shirt')
        self.assertContains(response, '$25.00')
        self.assertContains(response, 'In Stock')

        # Non-existent product returns 404
        response_404 = self.client.get(reverse('product_detail', args=[9999]))
        self.assertEqual(response_404.status_code, 404)

    # 5. User Registration, Login, and Logout
    def test_user_authentication_flow(self):
        # Test Registration
        reg_response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow=True)
        self.assertEqual(reg_response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Test Logout
        logout_response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(logout_response.status_code, 200)

        # Test Login with correct credentials
        login_response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(login_response.status_code, 200)
        self.assertContains(login_response, 'newuser')

    # 6. Shopping Cart Operations (Add, Increase, Decrease, Remove, Total)
    def test_cart_operations(self):
        # Add 2 units of p1
        self.client.post(reverse('add_to_cart', args=[self.p1.id]), {'quantity': 2})
        # Add 1 unit of p2
        self.client.post(reverse('add_to_cart', args=[self.p2.id]), {'quantity': 1})

        cart_page = self.client.get(reverse('cart'))
        self.assertEqual(cart_page.status_code, 200)
        self.assertContains(cart_page, 'Test Cotton Shirt')
        self.assertContains(cart_page, 'Test Sports Shoes')
        # Total: (2 * 25.00) + (1 * 80.00) = 130.00
        self.assertContains(cart_page, '130.00')

        # Increase quantity of p1
        self.client.get(reverse('increase_quantity', args=[self.p1.id]))
        cart_after_inc = self.client.get(reverse('cart'))
        # Total: (3 * 25.00) + (1 * 80.00) = 155.00
        self.assertContains(cart_after_inc, '155.00')

        # Decrease quantity of p1
        self.client.get(reverse('decrease_quantity', args=[self.p1.id]))
        cart_after_dec = self.client.get(reverse('cart'))
        # Total back to 130.00
        self.assertContains(cart_after_dec, '130.00')

        # Remove p2 from cart
        self.client.get(reverse('remove_from_cart', args=[self.p2.id]))
        cart_after_remove = self.client.get(reverse('cart'))
        # Total: 2 * 25.00 = 50.00
        self.assertContains(cart_after_remove, '50.00')

    # 7. Checkout, Order Creation & Inventory Stock Deduction
    def test_checkout_and_order_processing(self):
        # Add product to cart
        self.client.post(reverse('add_to_cart', args=[self.p1.id]), {'quantity': 2})

        # Submit checkout
        checkout_data = {
            'full_name': 'Alice Wonder',
            'email': 'alice@example.com',
            'phone': '1234567890',
            'address': '10 Downing St',
            'city': 'London',
            'state': 'Greater London',
            'zip_code': 'SW1A 2AA',
            'payment_method': 'COD'
        }
        process_response = self.client.post(reverse('process_order'), checkout_data, follow=True)
        self.assertEqual(process_response.status_code, 200)

        # Check Order was saved in DB
        order = Order.objects.get(email='alice@example.com')
        self.assertEqual(order.full_name, 'Alice Wonder')
        self.assertEqual(order.total_price, Decimal('50.00'))
        self.assertEqual(order.items.count(), 1)

        # Check OrderItem
        item = order.items.first()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal('25.00'))
        self.assertEqual(item.subtotal, Decimal('50.00'))

        # Check inventory was deducted from 10 to 8
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, 8)

        # Check cart was cleared
        cart_response = self.client.get(reverse('cart'))
        self.assertContains(cart_response, 'Your cart is currently empty')

    # 8. Django Admin Panel Access
    def test_admin_panel_access(self):
        # Non-logged in access redirects to admin login
        resp_unauth = self.client.get('/admin/')
        self.assertEqual(resp_unauth.status_code, 302)

        # Superuser login
        self.client.login(username='adminuser', password='adminpassword123')
        resp_admin = self.client.get('/admin/')
        self.assertEqual(resp_admin.status_code, 200)
        self.assertContains(resp_admin, 'Products')
        self.assertContains(resp_admin, 'Orders')
