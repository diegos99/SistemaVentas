from django.forms import ModelForm
#from django import forms
from .models import tipocliente , cliente, suscripcion

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
		#widgets = {
		#	'fecha_expiracion': forms.widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type':'datetime-local'}),
		#	'fecha_creacion': forms.widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type':'datetime-local'}),
			# 'fecha_expiracion': forms.DateInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'form-control', 'id':'Date', 'type':'datetime-local'}),
			# 'fecha_creacion': forms.DateInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'form-control', 'id':'Date1', 'type':'datetime-local'}),
			
		#	'cliente': forms.Select(attrs={'class': 'form-control'}),
		#	}