from .models.categoria import CategoriaPr, CategoriaProv
from .models.producto import Producto
from .models.proveedor import Proveedor

""" class CategoriaPr(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class CategoriaProv(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    
    nombre = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de venta
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    categoriaPr = models.ForeignKey(CategoriaPr, on_delete=models.CASCADE, related_name="productos", null=True, blank=True)
    

class Proveedor(models.Model):
    nombreProveedor = models.CharField(max_length=50)
    categoriaProv = models.ForeignKey(CategoriaProv, on_delete=models.CASCADE, related_name="proveedores", null=True, blank=True)
    costoInsumo = models.FloatField()
    tiempoEntrega = models.IntegerField() """
    