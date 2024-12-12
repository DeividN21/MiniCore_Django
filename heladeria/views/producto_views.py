from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from heladeria.models import Producto, CategoriaPr

@login_required
def consultar(request):
    productos = Producto.objects.all()
    categorias = CategoriaPr.objects.all()
    return render(request,"productos.html",{'productos' : productos, 'categorias': categorias})

def guardar(request):
    nombre = request.POST["nombre"]
    precio = request.POST["precio"]
    costo = request.POST["costo"]
    cantidad = request.POST["cantidad"]
    categoria_id = request.POST["categoria"]
    categoriaPr = CategoriaPr.objects.get(pk=categoria_id)
    descripcion = request.POST["descripcion"]
    p = Producto(nombre=nombre, precio=precio,costo=costo,cantidad=cantidad,categoriaPr=categoriaPr,descripcion=descripcion)
    p.save()
    messages.success(request,'Producto agregado!')
    return redirect('consultar')

def eliminar(request, id):
    producto = Producto.objects.filter(pk=id)
    producto.delete()
    messages.success(request, 'Producto eliminado!')
    return redirect('consultar')

def detalle(request, id):
    producto = Producto.objects.get(pk=id)
    categorias = CategoriaPr.objects.all()
    return render(request, "productoEditar.html", {'producto' : producto, 'categorias': categorias})
    
def editar(request):
    nombre = request.POST["nombre"]
    precio = request.POST["precio"]
    costo = request.POST["costo"]
    cantidad = request.POST["cantidad"]
    categoria_id = request.POST["categoria"]
    descripcion = request.POST["descripcion"]
    categoriaPr = CategoriaPr.objects.get(pk=categoria_id)
    id = request.POST["id"]
    Producto.objects.filter(pk=id).update(id=id,nombre=nombre,precio=precio,costo=costo,cantidad=cantidad,categoriaPr=categoriaPr,descripcion=descripcion)
    messages.success(request, 'Producto actualizado con exito!')
    return redirect('consultar')