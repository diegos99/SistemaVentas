from django.contrib import admin

from .models import objeto, tipocliente, cliente, suscripcion, repuesto, fabrica, vehiculo, compatibilidad, administrador, vendedor, tipopago #, Factura, DetalleFactura

admin.site.register(objeto)
admin.site.register(tipocliente)
admin.site.register(cliente)
admin.site.register(suscripcion)
admin.site.register(repuesto)
admin.site.register(fabrica)
admin.site.register(vehiculo)
admin.site.register(compatibilidad)
admin.site.register(administrador)
admin.site.register(vendedor)
admin.site.register(tipopago)
#admin.site.register(Factura)
#admin.site.register(DetalleFactura)
# Register your models here.
