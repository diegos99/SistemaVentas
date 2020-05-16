from django.forms import ModelForm
#from django import forms
from .models import tipocliente , cliente, suscripcion, repuesto, fabrica, vehiculo, compatibilidad, PedidoRecibido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

# Form para hacer pedido
class Formu(forms.Form):
	
	fechaEnvio = forms.CharField(label='fechaEnvio', max_length=100)
	producto = forms.CharField(label='producto', max_length=100)
	descripcion = forms.CharField(label='descripcion', max_length=100)
	cantidad = forms.CharField(label='cantidad', max_length=100)

# Form para recibir productos de fabrica
class Formu2(ModelForm):
	class Meta:
		model = PedidoRecibido
		fields = '__all__'

class FormularioTipoCliente(ModelForm):
	class Meta:
		model = tipocliente
		fields = '__all__'

class FormularioCliente(ModelForm):
	class Meta:
		model = cliente
		fields = '__all__'

class FormularioSuscrip(ModelForm):
	class Meta:
		model = suscripcion
		fields = '__all__'

class FormularioFabricas(ModelForm):
	class Meta:
		model = fabrica
		fields = '__all__'

class FormularioRepuestos(ModelForm):
	class Meta:
		model = repuesto
		fields = '__all__'

class FormularioVehiculos(ModelForm):
	class Meta:
		model = vehiculo
		fields = '__all__'

class FormularioCompat(ModelForm):
	class Meta:
		model = compatibilidad
		fields = '__all__'

