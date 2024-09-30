from django.contrib import admin
from .models import Product, condition, Type4Heavy, style, typeof, size, color

admin.site.register(Product)
admin.site.register(condition)
admin.site.register(Type4Heavy)
admin.site.register(style)
admin.site.register(typeof)
admin.site.register(size)
admin.site.register(color)

# Register your models here.
