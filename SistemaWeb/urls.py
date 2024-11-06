from django.urls import path
from . import views   

#Login AbstractUser
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.vista_portada, name='portada'),
    path('contacto/',views.contacto,name='contacto'),
    path('nosotros/',views.nosotros,name='nosotros'),
    path('productos/',views.productos,name='productos'),
    path('agregar_producto/',views.agregar_producto, name='agregar_producto'),  # Añadir esta línea
    path('modificar/<int:id>/', views.modificar_producto, name='modificar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('proveedores/', views.crud_proveedores, name='crud_proveedores'),
    path('productos/contacto/', views.contacto, name='contacto_productos'),
    path('marca/', views.marca, name= 'marca' ),
    #path('registro/', views.registro_usuario, name='registro_usuario'),


    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name='register'),

    path('logout/', views.logout_view, name='logout')
]