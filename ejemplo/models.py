from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.
class objeto (models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=50)
	def unicode (self):
		return self.nombre

#TTIPO DE CLIENTE
class tipocliente (models.Model):
	descripcion = models.CharField(max_length=50)
	descuento = models.DecimalField(max_digits=5, decimal_places=2)
	def unicode (self):
		return self.descripcion
			

#CLIENTE
class cliente (models.Model):
	nit = models.IntegerField(unique=True)
	nombre = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	telefono = models.IntegerField(verbose_name='Telefono')
	patente = models.ImageField(blank=True, null=True)
	tipo = models.ForeignKey(tipocliente, on_delete=models.PROTECT)
	def unicode (self):
		return self.nombre
		
#SUSCRIPCION		
class suscripcion(models.Model):	
	fecha_creacion = models.DateField()
	fecha_expiracion = models.DateField()
	estado = models.CharField(max_length=40, default='vigente')
	cliente = models.ForeignKey(cliente, on_delete=models.PROTECT)
	def unicode (self):
		return self.estado
	
	def estadosuscripcion(self):
		hoy = datetime.date.today()
		dias = (self.fecha_expiracion - hoy).days
		return dias	

	def save(self, *args, **kwargs):
		if self.estadosuscripcion() < 0:
			self.estado = 'vencido'
			super(suscripcion, self).save(*args, **kwargs)
		else:
			self.estado = 'vigente'
			super(suscripcion, self).save(*args, **kwargs)
