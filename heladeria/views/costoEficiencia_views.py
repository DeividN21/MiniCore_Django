from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from heladeria.models import Proveedor, CategoriaProv
from django.http import JsonResponse
import json

@login_required
def consultarCostoEficiencia(request):
    # Muestra todas las categorías
    categorias = CategoriaProv.objects.all()
    return render(request, "costoEficiencia.html", {'categorias': categorias})

@login_required
def proveedores_por_categoria(request, categoria_id):
    if request.method == 'GET':
        proveedores = Proveedor.objects.filter(categoriaProv_id=categoria_id)
        proveedores_list = list(proveedores.values('id', 'nombreProveedor'))
        return JsonResponse(proveedores_list, safe=False)

@login_required
def calcularCostoEficiencia(request):
    if request.method == 'POST':
        # Parsear datos de la solicitud
        data = json.loads(request.body)
        categoria_id = data.get('categoria')
        proveedor1_id = data.get('proveedor1')
        proveedor2_id = data.get('proveedor2')

        # Validar la categoría y los proveedores
        categoria = CategoriaProv.objects.filter(id=categoria_id).first()
        proveedor1 = Proveedor.objects.filter(id=proveedor1_id, categoriaProv=categoria).first()
        proveedor2 = Proveedor.objects.filter(id=proveedor2_id, categoriaProv=categoria).first()

        if not categoria or not proveedor1 or not proveedor2:
            return JsonResponse({'error': 'Categoría o proveedores inválidos'}, status=400)

        # Calcular el costo total y tiempo total
        costo_total = proveedor1.costoInsumo + proveedor2.costoInsumo
        tiempo_total = proveedor1.tiempoEntrega + proveedor2.tiempoEntrega

        # Calcular la eficiencia para cada proveedor
        eficiencia1 = ((proveedor1.costoInsumo / costo_total) * 50) + ((proveedor1.tiempoEntrega / tiempo_total) * 50)
        eficiencia2 = ((proveedor2.costoInsumo / costo_total) * 50) + ((proveedor2.tiempoEntrega / tiempo_total) * 50)

        # Determinar el proveedor más eficiente
        proveedor_mas_eficiente = proveedor1.nombreProveedor if eficiencia1 < eficiencia2 else proveedor2.nombreProveedor

        # Enviar resultados en JSON
        return JsonResponse({
            'proveedor1': {
                'costo': proveedor1.costoInsumo,
                'tiempo': proveedor1.tiempoEntrega,
                'eficiencia': round(eficiencia1, 2),
            },
            'proveedor2': {
                'costo': proveedor2.costoInsumo,
                'tiempo': proveedor2.tiempoEntrega,
                'eficiencia': round(eficiencia2, 2),
            },
            'resultado': f"{proveedor_mas_eficiente} es el proveedor más eficiente con respecto al costo-eficiencia.",
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)
