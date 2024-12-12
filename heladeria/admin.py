from django.contrib import admin
from heladeria.models import Producto,Proveedor, CategoriaPr,CategoriaProv

# Register your models here.
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(CategoriaPr)
admin.site.register(CategoriaProv)
