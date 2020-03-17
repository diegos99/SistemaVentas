from __future__ import unicode_literals

from django.db import models

# Create your models here.
class objeto (models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=50)
	def unicode (self):
		return self.nombre	
			


class cliente (models.Model):
	nit = models.IntegerField(unique=True)
	nombre = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	telefono = models.IntegerField(verbose_name='Telefono')
	patente = models.CharField(max_length=60)
	tipo = models.ForeignKey(objeto, on_delete=models.PROTECT)
	def unicode (self):
		return self.nombre
		
			
class suscripcion(models.Model):	
	estado = models.CharField(max_length=40)
	fecha_expiracion = models.DateField()
	fecha_creacion = models.DateField()
	cliente = models.ForeignKey(cliente, on_delete=models.PROTECT)
	def unicode (self):
		return self.estado
	
	def estadosuscripcion(self):
		hoy = datetime.date.today()
		dias = (self.fecha_expiracion - hoy).days
		return dias	

