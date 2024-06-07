from django.contrib import admin
from .models import Producto
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'medida','precio_contado', 'precio_lista', 'codigo_proveedor')
    list_filter = ('categoria',)

admin.site.register(Producto, ProductoAdmin)