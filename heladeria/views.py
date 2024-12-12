""" from django.shortcuts import render, redirect
from heladeria.models import Producto, Proveedor, CategoriaPr, CategoriaProv
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg
import json

# Create your views here.

def iniciar(request):
    if request.method=='GET':
        return render(request,"iniciar.html", {'form': AuthenticationForm})
    else:
        name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=name,password=password)
        if user is None:
            messages.success(request,'Usuario y/o contraseña incorrecto!')
            return render(request,"iniciar.html", {'form': AuthenticationForm})
        else:
            login(request,user)
            return redirect('inicio')
        

def registro(request):
    if request.method=='GET':
        return render(request, "registro.html", {'form': UserCreationForm})
    else:
        if request.POST["password1"] != request.POST["password2"]:
            messages.error(request,'Las contraseñas no coinciden!')
            return render(request, "registro.html", {'form': UserCreationForm})
        else:
            name = request.POST["username"]
            password = request.POST["password2"]
            user = User.objects.create_user(username=name,password=password)
            user.save()
            messages.success(request,'Usuario creado con éxito!')
            return render(request, "registro.html", {'form': UserCreationForm})
            
@login_required
def home(request):
    return render(request,"principal.html")

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

@login_required
def consultarP(request):
    proveedores = Proveedor.objects.all()
    categorias = CategoriaProv.objects.all()
    return render(request,"proveedores.html",{'proveedores' : proveedores,'categorias' : categorias})

def guardarP(request):
    nombreProveedor = request.POST["nombreProveedor"]
    categoria_id = request.POST["categoria"]
    costoInsumo = request.POST["costoInsumo"]
    tiempoEntrega = request.POST["tiempoEntrega"]
    categoriaProv = CategoriaProv.objects.get(pk=categoria_id)
    pr = Proveedor(nombreProveedor=nombreProveedor, categoriaProv=categoriaProv,
                   costoInsumo=costoInsumo,tiempoEntrega=tiempoEntrega)
    pr.save()
    messages.success(request,'Proveedor agregado!')
    return redirect('consultarP')

def eliminarP(request, id):
    proveedor = Proveedor.objects.filter(pk=id)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado!')
    return redirect('consultarP')

def detalleP(request, id):
    proveedor = Proveedor.objects.get(pk=id)
    categorias = CategoriaProv.objects.all()
    return render(request, "proveedorEditar.html", {'proveedor' : proveedor, 'categorias' : categorias})

def editarP(request):
    nombreProveedor = request.POST["nombreProveedor"]
    categoria_id = request.POST["categoria"]
    costoInsumo = request.POST["costoInsumo"]
    tiempoEntrega = request.POST["tiempoEntrega"]
    categoriaProv = CategoriaProv.objects.get(pk=categoria_id)
    id = request.POST["id"]
    Proveedor.objects.filter(pk=id).update(id=id,nombreProveedor=nombreProveedor,categoriaProv=categoriaProv,
                                            costoInsumo=costoInsumo,tiempoEntrega=tiempoEntrega)
    messages.success(request, 'Proveedor actualizado con exito!')
    return redirect('consultarP')

@login_required
def consultarRentabilidad(request):
    productos = Producto.objects.all()
    categorias = CategoriaPr.objects.all()
    return render(request, "rentabilidad.html", {'productos' : productos, 'categorias': categorias})

@login_required
def consultarCostoEficiencia(request):
    return render(request, "costoEficiencia.html")

def salir(request):
    logout(request)
    return redirect('iniciar')

@login_required
def calcular_rentabilidad(request):
    try:
        # Parsear el cuerpo de la solicitud como JSON
        data = json.loads(request.body)
        categoria1_id = data.get('categoria1')
        categoria2_id = data.get('categoria2')

        try:
            categoria1 = CategoriaPr.objects.get(pk=categoria1_id)
            categoria2 = CategoriaPr.objects.get(pk=categoria2_id)

            # Calcular los productos de cada categoría
            productos_categoria1 = Producto.objects.filter(categoriaPr=categoria1)
            productos_categoria2 = Producto.objects.filter(categoriaPr=categoria2)

            # Calcular el costo promedio de cada categoría
            costo_promedio_categoria1 = sum([producto.costo for producto in productos_categoria1]) / len(productos_categoria1) if productos_categoria1 else 0
            costo_promedio_categoria2 = sum([producto.costo for producto in productos_categoria2]) / len(productos_categoria2) if productos_categoria2 else 0

            # Calcular el precio de venta promedio de cada categoría
            precio_promedio_categoria1 = sum([producto.precio for producto in productos_categoria1]) / len(productos_categoria1) if productos_categoria1 else 0
            precio_promedio_categoria2 = sum([producto.precio for producto in productos_categoria2]) / len(productos_categoria2) if productos_categoria2 else 0

            # Calcular la rentabilidad de cada categoría
            rentabilidad_categoria1 = precio_promedio_categoria1 - costo_promedio_categoria1
            rentabilidad_categoria2 = precio_promedio_categoria2 - costo_promedio_categoria2

            # Determinar cuál categoría es más rentable
            if rentabilidad_categoria1 > rentabilidad_categoria2:
                categoria_mas_rentable = categoria1.nombre
                rentabilidad = rentabilidad_categoria1
            else:
                categoria_mas_rentable = categoria2.nombre
                rentabilidad = rentabilidad_categoria2

            # Preparar los datos para enviar de vuelta
            resultado = {
                'categoria1': {
                    'costo_promedio': costo_promedio_categoria1,
                    'precio_promedio': precio_promedio_categoria1,
                    'rentabilidad': rentabilidad_categoria1
                },
                'categoria2': {
                    'costo_promedio': costo_promedio_categoria2,
                    'precio_promedio': precio_promedio_categoria2,
                    'rentabilidad': rentabilidad_categoria2
                },
                'resultado': {
                    'categoria_mas_rentable': categoria_mas_rentable,
                    'rentabilidad': rentabilidad
                }
            }

            return JsonResponse(resultado)

        except CategoriaPr.DoesNotExist:
            return JsonResponse({'error': 'Categorías no válidas'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Ocurrió un error: {str(e)}'}, status=400) """
        
from .views.login_views import iniciar, registro, home, salir
from .views.producto_views import consultar, guardar, eliminar, detalle, editar
from .views.proveedor_views import consultarP, guardarP, eliminarP, detalleP, editarP
from .views.rentabilidad_views import consultarRentabilidad, calcular_rentabilidad
from .views.costoEficiencia_views import consultarCostoEficiencia