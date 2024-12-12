from django.db import models
from .categoria import CategoriaProv

class Proveedor(models.Model):
    nombreProveedor = models.CharField(max_length=50)
    categoriaProv = models.ForeignKey(CategoriaProv, on_delete=models.CASCADE, related_name="proveedores", null=True, blank=True)
    costoInsumo = models.FloatField()
    tiempoEntrega = models.IntegerField()
