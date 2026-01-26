#!/usr/bin/env python
"""
Script para corregir: eliminar el perfil de Cliente del vendedor
Ejecutar con: python manage.py shell < corregir_vendedor_cliente.py
"""

from django.contrib.auth.models import User
from gestion.models import Cliente

# Buscar el usuario vendedor
try:
    vendedor_user = User.objects.get(username='vendedor1')
    
    # Eliminar el perfil de Cliente si existe
    try:
        cliente_vendedor = Cliente.objects.get(user=vendedor_user)
        cliente_vendedor.delete()
        print(f"✅ Eliminado perfil de Cliente del vendedor {vendedor_user.username}")
    except Cliente.DoesNotExist:
        print(f"ℹ️  El vendedor {vendedor_user.username} no tiene perfil de Cliente")
    
    print(f"\n✅ Vendedor corregido:")
    print(f"   Username: {vendedor_user.username}")
    print(f"   Tiene inmuebles: {vendedor_user.inmuebles_registrados.exists()}")
    print(f"   Perfil de Cliente: NO")
    
except User.DoesNotExist:
    print("❌ No se encontró el usuario vendedor1")
