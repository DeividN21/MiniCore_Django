""" from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def pedidos(request):
    return render(request,"pedidos.html")

def salir(request):
    logout(request)
    return redirect('iniciar')
 """
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from heladeria.models import Pedido, Proveedor


@login_required
def consultarPedidos(request):
    pedidos = Pedido.objects.all()
    proveedores = Proveedor.objects.all()
    pedidos_mas_rapidos = []
    tiempo_mas_rapido = None

    # Filtrado por fechas
    if request.method == "POST" and 'filtrar' in request.POST:
        fecha_inicial = request.POST.get('fechaInicial')
        fecha_final = request.POST.get('fechaFinal')
        if fecha_inicial and fecha_final:
            pedidos = pedidos.filter(fechaPedido__range=[fecha_inicial, fecha_final])

        # Calcular proveedores más rápidos
        if pedidos.exists():
            menor_tiempo_entrega = float('inf')
            for pedido in pedidos:
                tiempo_entrega = (pedido.fechaEntrega - pedido.fechaPedido).days
                if tiempo_entrega < menor_tiempo_entrega:
                    menor_tiempo_entrega = tiempo_entrega
                    pedidos_mas_rapidos = [(pedido.nombreProveedorPedido, pedido.pedidoProducto)]
                    tiempo_mas_rapido = tiempo_entrega
                elif tiempo_entrega == menor_tiempo_entrega:
                    pedidos_mas_rapidos.append((pedido.nombreProveedorPedido, pedido.pedidoProducto))

    return render(request, "pedidos.html", {
        'pedidos': pedidos,
        'proveedores': proveedores,
        'pedidos_mas_rapidos': pedidos_mas_rapidos,
        'tiempo_mas_rapido': tiempo_mas_rapido
    })


@login_required
def guardarPedido(request):
    if request.method == "POST":
        pedidoProducto = request.POST["pedidoProducto"]
        fechaPedido = request.POST["fechaPedido"]
        fechaEntrega = request.POST["fechaEntrega"]
        nombreProveedorPedido_id = request.POST["nombreProveedorPedido"]
        nombreProveedorPedido = Proveedor.objects.get(pk=nombreProveedorPedido_id)

        pedido = Pedido(
            pedidoProducto=pedidoProducto,
            fechaPedido=fechaPedido,
            fechaEntrega=fechaEntrega,
            nombreProveedorPedido=nombreProveedorPedido
        )
        pedido.save()
        messages.success(request, 'Pedido agregado!')
        return redirect('consultarPedidos')

@login_required
def eliminarPedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    pedido.delete()
    messages.success(request, 'Pedido eliminado!')
    return redirect('consultarPedidos')

@login_required
def detallePedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    proveedores = Proveedor.objects.all()
    return render(request, "pedidoEditar.html", {'pedido': pedido, 'proveedores': proveedores})


@login_required
def editarPedido(request):
    if request.method == "POST":
        id = request.POST["id"]
        pedidoProducto = request.POST["pedidoProducto"]
        fechaPedido = request.POST["fechaPedido"]
        fechaEntrega = request.POST["fechaEntrega"]
        nombreProveedorPedido_id = request.POST["nombreProveedorPedido"]
        nombreProveedorPedido = Proveedor.objects.get(pk=nombreProveedorPedido_id)

        Pedido.objects.filter(pk=id).update(
            pedidoProducto=pedidoProducto,
            fechaPedido=fechaPedido,
            fechaEntrega=fechaEntrega,
            nombreProveedorPedido=nombreProveedorPedido
        )
        messages.success(request, 'Pedido actualizado con éxito!')
        return redirect('consultarPedidos')

