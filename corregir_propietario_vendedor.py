#!/usr/bin/env python
"""
Script para corregir: crear Propietario para el vendedor y actualizar el inmueble
Ejecutar con: python manage.py shell < corregir_propietario_vendedor.py
"""

from django.contrib.auth.models import User
from gestion.models import Propietario, Inmueble

# Buscar el usuario vendedor
try:
    vendedor_user = User.objects.get(username='vendedor1')
    
    # Verificar si ya existe un Propietario para el vendedor
    propietario_existente = Propietario.objects.filter(
        nombres='Juan',
        apellidos='Vendedor',
        email='vendedor@inmobicasita.com'
    ).first()
    
    if propietario_existente:
        print(f"ℹ️  Ya existe un Propietario para el vendedor: {propietario_existente}")
        propietario_vendedor = propietario_existente
    else:
        # Crear Propietario para el vendedor
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
        print(f"✅ Creado Propietario para el vendedor: {propietario_vendedor}")
    
    # Actualizar el inmueble para que el propietario sea el vendedor
    inmuebles = Inmueble.objects.filter(usuario=vendedor_user)
    if inmuebles.exists():
        for inmueble in inmuebles:
            inmueble.propietario = propietario_vendedor
            inmueble.save()
            print(f"✅ Actualizado inmueble {inmueble.codigo_interno} con propietario {propietario_vendedor}")
    else:
        print("⚠️  El vendedor no tiene inmuebles registrados")
    
    print(f"\n✅ Vendedor corregido:")
    print(f"   Username: {vendedor_user.username}")
    print(f"   Propietario: {propietario_vendedor.nombres} {propietario_vendedor.apellidos}")
    print(f"   Inmuebles: {inmuebles.count()}")
    
except User.DoesNotExist:
    print("❌ No se encontró el usuario vendedor1")
