from django.contrib import admin
from .models import Product, User, Order

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)