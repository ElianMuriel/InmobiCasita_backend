from django.contrib import admin
from .models import Rol, Propietario, Cliente, TipoInmueble, Inmueble, Visita, Contrato, Pago

admin.site.register(Rol)
admin.site.register(Propietario)
admin.site.register(Cliente)
admin.site.register(TipoInmueble)
admin.site.register(Inmueble)
admin.site.register(Visita)
admin.site.register(Contrato)
admin.site.register(Pago)
