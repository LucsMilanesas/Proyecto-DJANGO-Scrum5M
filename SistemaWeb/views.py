from django.shortcuts import render, redirect, get_object_or_404
#from django.http import HttpResponse
from .models import Producto, Proveedor, Marca, Usuarios
from .forms import ProductoForm, ProveedorForm, MarcaForm, UsuarioRegistroForm

def base(request):
    pro = Producto.objects.all()[:4]
    return render(request, 'base.html', {'Productos': pro})

def vista_portada(request):
    pro = Producto.objects.all()[:4]
    return render(request, 'portada.html', {'Productos': pro})

def contacto(request):
    return render(request, 'contacto.html')

def nosotros(request):
    return render(request, 'nosotros.html')


def agregar_producto(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES)  # Maneja archivos (ej. imágenes)
        if formulario.is_valid():
            formulario.save()  # Guarda el producto en la base de datos
            return redirect('productos')  # Redirige a la lista de productos después de guardar
    else:
        formulario = ProductoForm()  # Si no es POST, crea un formulario vacío
    
    context = {
        'formulario': formulario,
    }
    
    return render(request, 'agregar_producto.html', context)


def productos(request):
    pro = Producto.objects.all()  # Consulta todos los productos
    formulario = ProductoForm()  # Crea un formulario vacío (solo para agregar productos)
    
    context = {
        'formulario': formulario,
        'Productos': pro,
    }
    
    return render(request, 'productos.html', context)


def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)  # Busca el producto o lanza un error 404
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)  # Carga el producto en el formulario
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('productos')  # Redirige a la lista de productos después de modificar
    else:
        form = ProductoForm(instance=producto)  # Rellena el formulario con los datos del producto
    
    return render(request, 'modificar_producto.html', {'form': form})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)  # Busca el producto o lanza un error 404
    if request.method == 'POST':  # Solo si es una petición POST se elimina el producto
        producto.delete()  # Elimina el producto de la base de datos
        return redirect('productos')  # Redirige a la lista de productos después de eliminar
    
    return render(request, 'confirmar_eliminar.html', {'producto': producto})

def crud_proveedores(request):
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores

    if request.method == 'POST':

        if 'crear' in request.POST:
            formulario = ProveedorForm(request.POST)
            if formulario.is_valid():
                formulario.save()  # Guarda el nuevo proveedor
                return redirect('crud_proveedores')  # Redirige a la misma vista
            
        elif 'editar' in request.POST:
            proveedor_id = request.POST.get('proveedor_id')
            proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            formulario = ProveedorForm(request.POST, instance=proveedor)  # Cargar el proveedor existente
            if formulario.is_valid():
                formulario.save()  # Actualiza el proveedor
                return redirect('crud_proveedores')  # Redirige a la misma vista
            
        elif 'eliminar' in request.POST:
            proveedor_id = request.POST.get('proveedor_id')
            proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            proveedor.delete()  # Elimina el proveedor
            return redirect('crud_proveedores')  # Redirige a la misma vista
        
    else:
        formulario = ProveedorForm()  # Crear un formulario vacío para agregar


    # Si es una petición GET, verifica si hay un proveedor a editar
    proveedor_id = request.GET.get('proveedor_id')
    if proveedor_id:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        formulario = ProveedorForm(instance=proveedor)  # Cargar el proveedor para editar


    return render(request, 'crud_proveedores.html', {
        'proveedores': proveedores,
        'formulario': formulario
    })

def marca(request):
    if request.method == 'POST':
        formarca = MarcaForm(request.POST, request.FILES)
        if formarca.is_valid():
            formarca.save()
            return redirect('marca')
    else:
        formarca =  MarcaForm()
    context = {
        'formarca': formarca,
    }
    return render(request, 'marca.html', context)

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            # Guarda el usuario en la base de datos
            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.contraseña = form.cleaned_data['contraseña']  # Asegúrate de encriptar la contraseña
            nuevo_usuario.save()  # Guarda el usuario

            # Aquí podrías agregar la lógica para iniciar sesión automáticamente si lo deseas
            return redirect('portada')  # Redirige al login después del registro exitoso
    else:
        form = UsuarioRegistroForm()

    return render(request, 'registro.html', {'form': form})