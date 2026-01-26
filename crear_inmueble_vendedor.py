#!/usr/bin/env python
"""
Script para crear un inmueble para el vendedor
Ejecutar con: python manage.py shell < crear_inmueble_vendedor.py
"""

from django.contrib.auth.models import User
from gestion.models import Propietario, TipoInmueble, Inmueble

# Buscar el usuario vendedor
vendedor_user = User.objects.get(username='vendedor1')

# Obtener o crear Propietario para el vendedor
propietario_vendedor, _ = Propietario.objects.get_or_create(
    identificacion='1234567890',
    defaults={
        'nombres': 'Juan',
        'apellidos': 'Vendedor',
        'email': 'vendedor@inmobicasita.com',
        'telefono': '3001234567',
        'direccion': 'Calle 123',
        'ciudad': 'Bogotá',
        'activo': True
    }
)

# Obtener o crear tipo de inmueble
tipo_inmueble, _ = TipoInmueble.objects.get_or_create(
    nombre_tipo='Apartamento',
    defaults={'descripcion': 'Apartamento estándar', 'activo': True}
)

# Crear un inmueble para el vendedor
inmueble = Inmueble.objects.create(
    tipo=tipo_inmueble,
    propietario=propietario_vendedor,
    usuario=vendedor_user,  # Esto hace que sea VENDEDOR
    titulo='Apartamento en el centro',
    descripcion='Hermoso apartamento de 2 habitaciones en el centro de la ciudad',
    direccion='Carrera 7 # 45-23',
    ciudad='Bogotá',
    barrio='Centro',
    tipo_operacion='VENTA',
    precio_venta=250000000,
    numero_habitaciones=2,
    numero_banos=1,
    area_m2=65.5,
    estado='DISPONIBLE'
)

print(f"✅ Inmueble creado para el vendedor:")
print(f"   Código: {inmueble.codigo_interno}")
print(f"   Título: {inmueble.titulo}")
print(f"   Usuario: {inmueble.usuario.username}")
print(f"   Propietario: {inmueble.propietario.nombres} {inmueble.propietario.apellidos}")

# Verificar
inmuebles_count = Inmueble.objects.filter(usuario=vendedor_user).count()
print(f"\n✅ Total de inmuebles del vendedor: {inmuebles_count}")
