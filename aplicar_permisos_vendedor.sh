#!/bin/bash
# Script para aplicar permisos de vendedor en views.py

cd /opt/inmobicasita

# Hacer backup
cp gestion/views.py gestion/views.py.backup.permisos.$(date +%Y%m%d_%H%M%S)

echo "⚠️  Este script requiere edición manual"
echo "📝 Necesitas agregar la clase IsAdminOrVendedorOrReadOnly después de IsAdminOrReadOnly"
echo "📝 Y cambiar permission_classes en InmuebleViewSet"
echo ""
echo "Ver el archivo aplicar_permisos_vendedor.py para el código completo"
