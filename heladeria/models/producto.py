from django.db import models
from .categoria import CategoriaPr

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de venta
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    categoriaPr = models.ForeignKey(CategoriaPr, on_delete=models.CASCADE, related_name="productos", null=True, blank=True)
