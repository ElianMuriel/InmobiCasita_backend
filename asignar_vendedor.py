#!/usr/bin/env python
"""
Script para asignar grupo Vendedor a un usuario
Ejecutar con: python manage.py shell < asignar_vendedor.py
O directamente en el shell de Django
"""

from django.contrib.auth.models import User, Group

# Obtener o crear grupo Vendedor
vendedor_group, created = Group.objects.get_or_create(name='Vendedor')
if created:
    print(f"✅ Grupo 'Vendedor' creado")
else:
    print(f"ℹ️  Grupo 'Vendedor' ya existe")

# Asignar grupo al usuario vendedor1
try:
    vendedor = User.objects.get(username='vendedor1')
    vendedor.groups.add(vendedor_group)
    vendedor.save()
    print(f"✅ Usuario {vendedor.username} asignado como Vendedor")
    print(f"   Grupos del usuario: {[g.name for g in vendedor.groups.all()]}")
except User.DoesNotExist:
    print("❌ No se encontró el usuario vendedor1")
