from django.urls import path
from . import views   

urlpatterns = [
    path('', views.vista_portada, name='portada'),
    path('contacto/',views.contacto,name='contacto'),
    path('nosotros/',views.nosotros,name='nosotros'),
    path('productos/',views.productos,name='productos'),
    path('agregar_producto/',views.agregar_producto, name='agregar_producto'),  # Añadir esta línea
    path('modificar/<int:id>/', views.modificar_producto, name='modificar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('proveedores/', views.crud_proveedores, name='crud_proveedores'),
]