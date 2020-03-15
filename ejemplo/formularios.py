from django.forms import ModelForm

from .models import objeto

class FormularioObjeto(ModelForm):
	class Meta:
		model = objeto
		fields = '__all__'