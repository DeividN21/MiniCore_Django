from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from heladeria.models import Producto, CategoriaPr
from django.http import JsonResponse
import json

@login_required
def consultarRentabilidad(request):
    productos = Producto.objects.all()
    categorias = CategoriaPr.objects.all()
    return render(request, "rentabilidad.html", {'productos': productos, 'categorias': categorias})

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
            costo_promedio_categoria1 = 0
            if productos_categoria1:
                suma_costo_categoria1 = 0
                for producto in productos_categoria1:
                    suma_costo_categoria1 += producto.costo
                costo_promedio_categoria1 = suma_costo_categoria1 / len(productos_categoria1)

            costo_promedio_categoria2 = 0
            if productos_categoria2:
                suma_costo_categoria2 = 0
                for producto in productos_categoria2:
                    suma_costo_categoria2 += producto.costo
                costo_promedio_categoria2 = suma_costo_categoria2 / len(productos_categoria2)

            # Calcular el precio de venta promedio de cada categoría
            precio_promedio_categoria1 = 0
            if productos_categoria1:
                suma_precio_categoria1 = 0
                for producto in productos_categoria1:
                    suma_precio_categoria1 += producto.precio
                precio_promedio_categoria1 = suma_precio_categoria1 / len(productos_categoria1)

            precio_promedio_categoria2 = 0
            if productos_categoria2:
                suma_precio_categoria2 = 0
                for producto in productos_categoria2:
                    suma_precio_categoria2 += producto.precio
                precio_promedio_categoria2 = suma_precio_categoria2 / len(productos_categoria2)

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
        return JsonResponse({'error': f'Ocurrió un error: {str(e)}'}, status=400)