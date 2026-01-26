#!/bin/bash
# Script para completar los cambios de vendedor en views.py

cd /opt/inmobicasita

# Hacer backup
cp gestion/views.py gestion/views.py.backup.$(date +%Y%m%d_%H%M%S)

# 1. Agregar Group al import (si no está)
if ! grep -q "from django.contrib.auth.models import User, Group" gestion/views.py; then
    sed -i 's/from django.contrib.auth.models import User/from django.contrib.auth.models import User, Group/' gestion/views.py
    echo "✅ Import de Group agregado"
else
    echo "ℹ️  Import de Group ya existe"
fi

# 2. Cambiar la función register para usar grupos
sed -i "s/refresh\['is_vendedor'\] = Inmueble.objects.filter(usuario=user).exists()/refresh['is_vendedor'] = user.groups.filter(name='Vendedor').exists()/g" gestion/views.py

echo "✅ Cambios aplicados en views.py"
echo "📝 Verificando cambios..."
grep -n "is_vendedor" gestion/views.py
