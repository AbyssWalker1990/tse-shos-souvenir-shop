from django.contrib import admin
from .models import Category, Product, Tag, OrderProduct, OrderCard
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(OrderProduct)
admin.site.register(OrderCard)

