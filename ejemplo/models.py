from __future__ import unicode_literals

from django.db import models, connection
from django.conf import settings
from django.db.models import signals
import datetime
import decimal
GASTOS_IMPORTACION = 0.15
IMPUESTOS = 0.30
COMISION = 0.05
GANANCIA = 0.40
IVA = 0.12


# Create your models here.
class objeto (models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=50)
	def unicode (self):
		return self.nombre

# TIPOS DE CLIENTE
class tipocliente (models.Model):
	descripcion = models.CharField(max_length=50)
	descuento = models.DecimalField(max_digits=5, decimal_places=2)
	def __str__ (self):
		return self.descripcion
	
			

# CLIENTES
class cliente (models.Model):
	nit = models.IntegerField(unique=True)
	nombre = models.CharField(max_length=60)
	email = models.CharField(max_length=60)
	telefono = models.IntegerField(verbose_name='Telefono')
	patente = models.ImageField(blank=True, null=True)
	tipo = models.ForeignKey(tipocliente, on_delete=models.PROTECT)
	def __str__ (self):
		return self.nombre
	
		
# SUSCRIPCIONES		
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

# FABRICAS
class fabrica (models.Model):
	nombre = models.CharField(max_length=100)
	ip = models.CharField(max_length=100)
	def __str__ (self):
		return self.nombre

# REPUESTOS
class repuesto(models.Model):
	nombre = models.CharField(max_length=400)
	descripcion = models.TextField(max_length=400)
	no_parte = models.IntegerField()
	fabrica = models.ForeignKey(fabrica, on_delete=models.PROTECT)
	stock = models.PositiveSmallIntegerField()
	precio_fabricante = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	precio_venta = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	igv = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	imagen = models.ImageField(blank=True, null=True)
	imagen2 = models.CharField(max_length=400, null=True)
	def __str__ (self):
		return U" %s- %s" % (self.nombre, self.descripcion)
	""" def __unicode__ (self):
		return self.id """

	def preeciototal(self):
		precio_total=self.precio_compra*self.stock
		return precio_total
		
	def save(self, *args, **kwargs):
		if self.precio_fabricante:
			calc1 = round((float(self.precio_fabricante) + (float(self.precio_fabricante) * GASTOS_IMPORTACION)), 2)
			calc2 = round((calc1 + (calc1 * IMPUESTOS)), 2)
			calc3 = round((calc2 + (calc2 * COMISION)), 2)
			self.precio_venta = round((calc3 + (calc3 * GANANCIA)), 2)
			self.igv = round((self.precio_venta * (IVA + GANANCIA)), 2)
			super(repuesto, self).save(*args, **kwargs)
		else:
			self.precio_venta=0
			self.igv=0
			super(repuesto, self).save(*args, **kwargs)

# VEHICULOS
class vehiculo (models.Model):
	marca = models.CharField(max_length=100)
	linea = models.CharField(max_length=100)
	anio = models.IntegerField()
	def __str__ (self):
		return U" %s- %s" % (self.marca, self.linea)
		""" return self.id """

# COMPATIBILIDAD --> REPUESTOS - VEHICULOS
class compatibilidad (models.Model):
	repuesto = models.ForeignKey(repuesto, on_delete=models.PROTECT)
	vehiculo = models.ForeignKey(vehiculo, on_delete=models.PROTECT)
	def unicode (self):
		return self.id

# ADMINISTRADOR
class administrador (models.Model):
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	telefono = models.IntegerField()
	def __str__ (self):
		return self.username

# VENDEDOR
class vendedor (models.Model):
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	telefono = models.IntegerField()
	administrador = models.ForeignKey(administrador, on_delete=models.PROTECT)
	def __str__ (self):
		return self.username

# TIPO DE PAGO
class tipopago (models.Model):
	pago = models.CharField(max_length=100)
	def __str__ (self):
		return self.pago





# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

# ORDEN DE COMPRA
class Orden(models.Model):
	cliente = models.ForeignKey(cliente, null=True, blank=True, on_delete=models.PROTECT)
	total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	fecha = models.DateField(auto_now_add=True)
	def __unicode__ (self):
		return self.id

# DETALLE ORDEN DE COMPRA
class DetalleOrden(models.Model):
	orden = models.ForeignKey(Orden, db_column='orden_id', related_name='orden', on_delete=models.PROTECT)
	producto = models.ForeignKey(repuesto, db_column='repuesto_id', on_delete=models.PROTECT)
	descripcion = models.CharField(max_length=40)
	fabrica = models.ForeignKey(fabrica, null=True, blank=True, on_delete=models.PROTECT)
	precio = models.DecimalField(max_digits=6, decimal_places=2)
	cantidad = models.IntegerField()
	impuesto = models.DecimalField(max_digits=6, decimal_places=2)
	subtotal = models.DecimalField(max_digits=6, decimal_places=2)
	def __unicode__ (self):
		return self.descripcion
	
	def suma(self):
		return self.cantidad * self.producto.precio_venta



#  FACTURA
class Factura(models.Model):
	orden = models.ForeignKey(Orden, null=True, blank=True, on_delete=models.PROTECT)
	cliente = models.ForeignKey(cliente, db_column='cliente_id', on_delete=models.PROTECT)
	total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	fecha = models.DateField(auto_now_add=True)
	def __unicode__ (self):
		return self.id


# DETALLE
class DetalleFactura(models.Model):
	factura = models.ForeignKey(Factura, db_column='factura_id', related_name='factura', on_delete=models.PROTECT)
	detalleorden = models.ForeignKey(DetalleOrden, db_column='detalleorden_id', related_name='detalleorden', on_delete=models.PROTECT)
	producto = models.ForeignKey(repuesto, db_column='repuesto_id', on_delete=models.PROTECT)
	descripcion = models.CharField(max_length=40)
	fabrica = models.ForeignKey(fabrica, null=True, blank=True, on_delete=models.PROTECT)
	precio = models.DecimalField(max_digits=6, decimal_places=2)
	cantidad = models.IntegerField()
	impuesto = models.DecimalField(max_digits=6, decimal_places=2)
	subtotal = models.DecimalField(max_digits=6, decimal_places=2)
	def __unicode__ (self):
		return self.descripcion
	
	def suma(self):
		return self.cantidad * self.producto.precio_venta
	
def update_stock(sender, instance, **kwargs):
		instance.producto.stock -= instance.cantidad
		instance.producto.save()

signals.post_save.connect(update_stock, sender=DetalleFactura, dispatch_uid="update_stock_count")


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

# PEDIDOS
class PedidoRecibido(models.Model):
	producto = models.CharField(max_length=40)
	descripcion = models.CharField(max_length=40)
	cantidad = models.CharField(max_length=40)
	def __unicode__ (self):
		return self.producto