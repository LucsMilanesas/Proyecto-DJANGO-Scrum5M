from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Tipos(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre}"

class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    gmail = models.EmailField()
    usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    tipos = models.ForeignKey('Tipos', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def clean(self):
        super().clean()
        
        # Validación del DNI
        if not self.dni.isdigit() or len(self.dni) != 8:  # Asumiendo que el DNI tiene 8 dígitos
            raise ValidationError('El DNI debe tener 8 dígitos y ser numérico.')

        # Validación del teléfono
        if not self.telefono.isdigit():
            raise ValidationError('El teléfono debe ser numérico.')

        # Validación del campo de correo electrónico
        if not self.gmail.endswith('@gmail.com'):
            raise ValidationError('El correo electrónico debe ser una cuenta de Gmail.')

        # Validación de contraseña
        if len(self.contraseña) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')



class Caja(models.Model):
    #id_caja = models.AutoField(primary_key=True)
    fecha = models.DateField()
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_final = models.DecimalField(max_digits=10, decimal_places=2)
    Usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)

    def __str__(self):
        #return f"Caja {self.id_caja} - {self.fecha}"
    
        # Aquí usamos el campo 'id' que Django crea automáticamente
        return f"Caja {self.id} - {self.fecha} - Saldo Inicial: {self.saldo_inicial} - Saldo Final: {self.saldo_final}"

    
class Venta(models.Model):
    #id_venta = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    Usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"
    
class Marca(models.Model):
    #id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    #id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    #tipo = models.
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    stock = models.IntegerField(default=0)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Categoría
    imagen = models.ImageField(upload_to="productos", null=True)
    
    def save(self, *args, **kwargs):
            if self.pk is None:  # Encriptar la contraseña solo al crear un usuario nuevo
                self.contraseña = make_password(self.contraseña)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class DetalleVenta(models.Model):
    #id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    #def __str__(self):
        #return f'Detalle {self.id_detalle} - Venta: {self.venta.id_venta}'
    
    def __str__(self):
        return f'Detalle {self.id} - Venta {self.venta.id} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}'

class Pedido(models.Model):
    #id_pedido = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    #cantidad = models.PositiveIntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False)

    def __str__(self):
        return f'Pedido {self.id} - Usuario: {self.usuario.username}'
    
class ProductoPorPedido(models.Model):
    #id_producto_pedido = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Producto {self.producto.nombre} - Pedido: {self.pedido.id}'
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    #apellido = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

""" #Existe un Conflicto con esta parte del DER
class CompraProveedor(models.Model):
    #id_cp = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras')
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Compra {self.id} - Proveedor: {self.proveedor.nombre}'
    
class DetalleCompra(models.Model):
    #id_det_compra = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    compra_proveedor = models.ForeignKey(CompraProveedor, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Compra {self.id} - Producto: {self.pedido}" """