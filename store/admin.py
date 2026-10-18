from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Displays purchased items in a table directly inside the Order detail page.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Products.
    """
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')  # Enables fast inline updates in the list view
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for reviewing and managing Customer Orders.
    """
    list_display = ('id', 'full_name', 'email', 'phone', 'total_price', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'address', 'city')
    list_editable = ('status',)  # Change status (e.g. Pending -> Shipped) directly from list view
    inlines = [OrderItemInline]
    list_per_page = 20


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order Items.
    """
    list_display = ('id', 'order', 'product', 'price', 'quantity')
    list_filter = ('product', 'order__status')
    search_fields = ('order__full_name', 'product__name')
