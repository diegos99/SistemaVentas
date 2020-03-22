from django.contrib import admin

from .models import objeto, tipocliente, cliente, suscripcion

admin.site.register(objeto)
admin.site.register(tipocliente)
admin.site.register(cliente)
admin.site.register(suscripcion)
# Register your models here.
