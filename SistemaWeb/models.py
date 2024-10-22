from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empleado(models.Model):
    #DJango define automaticamente las PK si no se las asigna aqui
    #id_empleado = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    gmail = models.EmailField()
    usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Caja(models.Model):
    #id_caja = models.AutoField(primary_key=True)
    fecha = models.DateField()
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_final = models.DecimalField(max_digits=10, decimal_places=2)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        #return f"Caja {self.id_caja} - {self.fecha}"
    
        # Aquí usamos el campo 'id' que Django crea automáticamente
        return f"Caja {self.id} - {self.fecha} - Saldo Inicial: {self.saldo_inicial} - Saldo Final: {self.saldo_final}"
    
class Cliente(models.Model):
    #id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Venta(models.Model):
    #id_venta = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.nombre

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

""" #Este es el pedido del Proyecto
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Pedido {self.nombre}" """
    
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