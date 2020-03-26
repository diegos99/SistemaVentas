from django.forms import ModelForm
#from django import forms
from .models import tipocliente , cliente, suscripcion, repuesto, fabrica, vehiculo, compatibilidad

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