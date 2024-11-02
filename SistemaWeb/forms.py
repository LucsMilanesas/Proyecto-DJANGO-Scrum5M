from django import forms
from .models import Producto, Proveedor, Marca, Usuarios

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'nuevo', 'stock', 'marca', 'imagen'] 

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'email']

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']

class UsuarioRegistroForm(forms.ModelForm): 
    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'dni', 'domicilio', 'telefono', 'gmail', 'usuario', 'contraseña', 'tipos']

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        # Validación de coincidencia de contraseñas
        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            self.add_error("confirmar_contraseña", "Las contraseñas no coinciden.")

        # Validación de longitud de la contraseña
        if contraseña and len(contraseña) < 8:
            self.add_error("contraseña", "La contraseña debe tener al menos 8 caracteres.")

        return cleaned_data  # Devuelve cleaned_data para continuar con el procesamiento
 
