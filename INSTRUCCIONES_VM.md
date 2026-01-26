# Instrucciones para Aplicar Cambios en la VM

## Paso 1: Modificar `gestion/views.py`

### Opción A: Usando sed (automático)

```bash
cd /opt/inmobicasita
source venv/bin/activate

# Hacer backup
cp gestion/views.py gestion/views.py.backup

# Reemplazar la línea que detecta vendedor
sed -i "s/token\['is_vendedor'\] = bool(Inmueble.objects.filter(usuario=user).exists())/token['is_vendedor'] = bool(user.groups.filter(name='Vendedor').exists())/g" gestion/views.py

# Verificar el cambio
grep -n "is_vendedor" gestion/views.py
```

### Opción B: Editar manualmente

1. Abrir el archivo:
```bash
cd /opt/inmobicasita
nano gestion/views.py
```

2. Buscar la clase `CustomTokenObtainPairSerializer` (usa Ctrl+W para buscar)

3. Buscar esta línea:
```python
token['is_vendedor'] = bool(Inmueble.objects.filter(usuario=user).exists())
```

4. Reemplazarla por:
```python
token['is_vendedor'] = bool(user.groups.filter(name='Vendedor').exists())
```

5. Verificar que el import esté presente al inicio del archivo:
```python
from django.contrib.auth.models import Group
```

6. Si no está, agregarlo junto con los otros imports.

7. Guardar: Ctrl+O, Enter, Ctrl+X

## Paso 2: Asignar grupo Vendedor al usuario

```bash
cd /opt/inmobicasita
source venv/bin/activate
python manage.py shell
```

Y ejecutar:

```python
from django.contrib.auth.models import User, Group

# Crear o obtener grupo Vendedor
vendedor_group, created = Group.objects.get_or_create(name='Vendedor')
if created:
    print(f"✅ Grupo 'Vendedor' creado")
else:
    print(f"ℹ️  Grupo 'Vendedor' ya existe")

# Asignar grupo al usuario vendedor1
vendedor = User.objects.get(username='vendedor1')
vendedor.groups.add(vendedor_group)
vendedor.save()
print(f"✅ Usuario {vendedor.username} asignado como Vendedor")
print(f"   Grupos: {[g.name for g in vendedor.groups.all()]}")

# Salir
exit()
```

O usar el script:

```bash
cd /opt/inmobicasita
source venv/bin/activate
python manage.py shell < aplicar_cambios_vendedor.py
```

## Paso 3: Verificar que no hay errores

```bash
cd /opt/inmobicasita
source venv/bin/activate
python manage.py check
```

Debería mostrar: `System check identified no issues (0 silenced).`

## Paso 4: Reiniciar el servicio

```bash
sudo systemctl restart inmobicasita
sudo systemctl status inmobicasita
```

## Paso 5: Verificar logs

```bash
sudo journalctl -u inmobicasita -n 50 --no-pager
```

No debería haber errores.

## Verificación Final

1. Cerrar sesión en el frontend (si estás logueado)
2. Iniciar sesión como `vendedor1`
3. Debería redirigir a `/vendedor`
4. El dashboard y la lista de inmuebles deberían mostrar los mismos inmuebles
