from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('catalogo/',views.catalogo),
    path('nuevo_producto/',views.nuevo_producto),
    path('nuevo_producto/crear_producto',views.crear_producto),
    path('seguridad/',views.seguridad),
    path('nuevo_usuario/',views.nuevo_usuario),
    path('nuevo_usuario/crear_usuario',views.crear_usuario),
    path('validar_login',views.validar_login),
    path('proveedor/',views.proveedor),
    path('nuevo_proveedor/',views.nuevo_proveedor),
    path('nuevo_proveedor/crear_proveedor',views.crear_proveedor),
    path('ordenes/',views.ordenes),
    path('nueva_orden/',views.nueva_orden),
    path('nueva_orden/crear_orden',views.crear_orden),
    path('ordenes_completas/',views.ordenes_completas),
    path('orden_completa/',views.orden_completa),
    path('ventas/',views.venta),
    path('agregar_venta/',views.agregar_venta),
    path('agregar_venta/crear_venta',views.crear_venta),
]