from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from heladeria.models import Proveedor, CategoriaProv
from django.http import JsonResponse
import json


@login_required
def consultarCostoEficiencia(request):
    proveedores = Proveedor.objects.all()
    categorias = CategoriaProv.objects.all()
    return render(request, "costoEficiencia.html", {'proveedores': proveedores, 'categorias': categorias})