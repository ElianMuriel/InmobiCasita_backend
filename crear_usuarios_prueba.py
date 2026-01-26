#!/usr/bin/env python
"""
Script para crear usuarios de prueba: VENDEDOR y CLIENTE
Ejecutar con: python manage.py shell < crear_usuarios_prueba.py
O copiar y pegar en: python manage.py shell
"""

from django.contrib.auth.models import User
from gestion.models import Cliente, Propietario, TipoInmueble, Inmueble

# 1. Crear usuario VENDEDOR
print("Creando usuario VENDEDOR...")
vendedor_user = User.objects.create_user(
    username='vendedor1',
    password='vendedor123',
    email='vendedor@inmobicasita.com',
    first_name='Juan',
    last_name='Vendedor',
    is_staff=False,
    is_active=True
)

# NO crear perfil de Cliente para el vendedor
# Los vendedores se identifican por tener inmuebles registrados (campo usuario en Inmueble)

# Crear un Propietario para el vendedor (el vendedor también es propietario)
propietario_vendedor = Propietario.objects.create(
    nombres='Juan',
    apellidos='Vendedor',
    identificacion='1234567890',
    email='vendedor@inmobicasita.com',
    telefono='3001234567',
    direccion='Calle 123',
    ciudad='Bogotá',
    activo=True
)

# Obtener o crear tipo de inmueble
tipo_inmueble, _ = TipoInmueble.objects.get_or_create(
    nombre_tipo='Apartamento',
    defaults={'descripcion': 'Apartamento estándar', 'activo': True}
)

# Crear un inmueble para que el usuario sea VENDEDOR
inmueble = Inmueble.objects.create(
    tipo=tipo_inmueble,
    propietario=propietario_vendedor,  # El vendedor es también el propietario
    usuario=vendedor_user,  # Esto hace que sea VENDEDOR
    codigo_interno='APT-001',
    titulo='Apartamento en el centro',
    descripcion='Hermoso apartamento de 2 habitaciones',
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

print(f"✅ Usuario VENDEDOR creado:")
print(f"   Username: {vendedor_user.username}")
print(f"   Password: vendedor123")
print(f"   Propietario: {propietario_vendedor.nombres} {propietario_vendedor.apellidos}")
print(f"   Inmueble creado: {inmueble.codigo_interno}")
print(f"   NOTA: El vendedor NO tiene perfil de Cliente, pero SÍ es Propietario")

# 2. Crear usuario CLIENTE
print("\nCreando usuario CLIENTE...")
cliente_user = User.objects.create_user(
    username='cliente1',
    password='cliente123',
    email='cliente@inmobicasita.com',
    first_name='Carlos',
    last_name='Cliente',
    is_staff=False,
    is_active=True
)

# Crear perfil de Cliente (sin inmuebles, por eso es solo CLIENTE)
cliente_cliente = Cliente.objects.create(
    nombres='Carlos',
    apellidos='Cliente',
    identificacion='1122334455',
    email='cliente@inmobicasita.com',
    telefono='3001122334',
    direccion='Calle 789',
    ciudad='Medellín',
    tipo_cliente='COMPRADOR',
    activo=True,
    user=cliente_user
)

print(f"✅ Usuario CLIENTE creado:")
print(f"   Username: {cliente_user.username}")
print(f"   Password: cliente123")
print(f"   Cliente ID: {cliente_cliente.id}")

print("\n✅ Usuarios de prueba creados exitosamente!")
print("\nCredenciales:")
print("VENDEDOR:")
print("  Username: vendedor1")
print("  Password: vendedor123")
print("\nCLIENTE:")
print("  Username: cliente1")
print("  Password: cliente123")
