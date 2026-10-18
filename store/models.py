from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """
    Represents a product item in the StyleCart store.
    """
    CATEGORY_CHOICES = [
        ('Apparel', 'Apparel'),
        ('Footwear', 'Footwear'),
        ('Accessories', 'Accessories'),
        ('Bags', 'Bags'),
        ('Electronics', 'Electronics'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Apparel')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Order(models.Model):
    """
    Represents a customer's placed order with shipping and payment details.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Credit / Debit Card (Demo)'),
    ]

    # Optional foreign key to registered user; allows guest checkout if null
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Shipping & contact info
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    # Order details
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} (${self.total_price})"


class OrderItem(models.Model):
    """
    Represents an individual item purchased within an Order.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"
