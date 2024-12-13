from django.db import models
from .proveedor import Proveedor

class Pedido(models.Model):
    pedidoProducto = models.CharField(max_length=30)
    fechaPedido = models.DateField()
    fechaEntrega = models.DateField()
    nombreProveedorPedido = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="proovedores")
    