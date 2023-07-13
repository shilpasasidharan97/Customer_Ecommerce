from django.contrib import admin
from api.models import User, Product

# Register your models here.
admin.site.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Product, ProductAdmin)
