from django import forms
from .models import Producto, Proveedor, Marca, Usuarios

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'nuevo', 'stock', 'marca', 'categoria', 'imagen'] 

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'email']

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']


class UsuarioRegistroForm(forms.ModelForm): 
    #contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Usuarios
        #fields = ['nombre', 'apellido', 'dni', 'domicilio', 'telefono', 'gmail', 'usuario', 'contraseña', 'tipos']
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'dni', 'domicilio', 'telefono', 'tipos']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError('El DNI debe tener 8 dígitos y ser numérico.')
        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe ser numérico.')
        return telefono

    def clean_contraseña(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("password")
        confirmar_contraseña = cleaned_data.get("confirm_password")

        # Validación de coincidencia de contraseñas
        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")

        # Validación de longitud de la contraseña
        if contraseña and len(contraseña) < 8:
            self.add_error("password", "La contraseña debe tener al menos 8 caracteres.")

        return cleaned_data  # Devuelve cleaned_data para continuar con el procesamiento
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Cifra la contraseña
        if commit:
            user.save()
        return user
