"""
URL configuration for CRUD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from heladeria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.iniciar, name='iniciar'),
    path('registro/',views.registro, name='registro'),
    path('inicio', views.home, name='inicio'),
    path('productos', views.consultar, name='consultar'),
    path('productos/guardar', views.guardar, name='guardar'),
    path('productos/eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('productos/detalle/<int:id>', views.detalle, name='detalle'),
    path('productos/editar', views.editar, name='editar'),
    path('proveedores', views.consultarP, name='consultarP'),
    path('proveedores/guardar', views.guardarP, name='guardarP'),
    path('proveedores/eliminar/<int:id>', views.eliminarP, name='eliminarP'),
    path('proveedores/detalle/<int:id>', views.detalleP, name='detalleP'),
    path('proveedores/editar', views.editarP, name='editarP'),
    path('rentabilidad', views.consultarRentabilidad, name='consultarRentabilidad'),
    path('costoEficiencia', views.consultarCostoEficiencia, name='consultarCostoEficiencia'),
    path('salir/',views.salir, name='salir'),
    path('calcular-rentabilidad/', views.calcular_rentabilidad, name='calcular_rentabilidad'),
    path('calcular-costo-eficiencia/', views.calcularCostoEficiencia, name='calcular_costo_eficiencia'),
    path('proveedores-por-categoria/<int:categoria_id>/', views.proveedores_por_categoria, name='proveedores_por_categoria'),
    path('pedidos/', views.consultarPedidos, name='consultarPedidos'),
    path('pedidos/guardar/', views.guardarPedido, name='guardarPedido'),
    path('pedidos/eliminar/<int:id>/', views.eliminarPedido, name='eliminarPedido'),
    path('pedidos/detalle/<int:id>/', views.detallePedido, name='detallePedido'),
    path('pedidos/editar/', views.editarPedido, name='editarPedido'),
]
