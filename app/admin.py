from django.contrib import admin
from . models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist

# Register your models here.
@admin.register(Product)
class ProductModleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image', ]

@admin.register(Customer)
class CustomerModleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode', ]
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Payment)    
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'city', 'paid', 'updated',
    ]
    list_filter = ['paid', 'created', 'updated']
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']
    
    
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']