#!/usr/bin/env python
"""
Script para completar los cambios de vendedor
Ejecutar con: python manage.py shell < completar_cambios_vendedor.py
"""

from django.contrib.auth.models import User, Group

print("=" * 60)
print("COMPLETANDO CAMBIOS PARA VENDEDOR")
print("=" * 60)

# 1. Crear o obtener grupo Vendedor
vendedor_group, created = Group.objects.get_or_create(name='Vendedor')
if created:
    print(f"✅ Grupo 'Vendedor' creado")
else:
    print(f"ℹ️  Grupo 'Vendedor' ya existe")

# 2. Asignar grupo al usuario vendedor1
try:
    vendedor = User.objects.get(username='vendedor1')
    vendedor.groups.add(vendedor_group)
    vendedor.save()
    print(f"✅ Usuario {vendedor.username} asignado como Vendedor")
    print(f"   Grupos del usuario: {[g.name for g in vendedor.groups.all()]}")
except User.DoesNotExist:
    print("❌ No se encontró el usuario vendedor1")

# 3. Verificar otros usuarios que podrían ser vendedores
print("\n" + "=" * 60)
print("VERIFICACIÓN")
print("=" * 60)

# Contar usuarios en el grupo Vendedor
vendedores = User.objects.filter(groups__name='Vendedor')
print(f"✅ Total de vendedores: {vendedores.count()}")
for v in vendedores:
    print(f"   - {v.username}")

print("\n✅ Cambios completados correctamente")
