# Script para aplicar permisos de vendedor
# Copiar y pegar este código en el archivo gestion/views.py

# AGREGAR DESPUÉS de la clase IsAdminOrReadOnly:

"""
class IsAdminOrVendedorOrReadOnly(permissions.BasePermission):
    \"\"\"
    Lectura para todos.
    Crear / actualizar para admin (is_staff=True) y vendedores (grupo Vendedor).
    Eliminar solo para admin.
    \"\"\"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin puede hacer todo
        if request.user.is_staff:
            return True
        
        # Vendedor puede crear y editar, pero no eliminar
        if request.method == 'DELETE':
            return False  # Solo admin puede eliminar
        
        # Verificar si es vendedor
        from django.contrib.auth.models import Group
        vendedor_group = Group.objects.filter(name='Vendedor').first()
        if vendedor_group and request.user.groups.filter(name='Vendedor').exists():
            return True  # Vendedor puede crear y editar
        
        return False
"""

# CAMBIAR en InmuebleViewSet:
# permission_classes = [IsAdminOrReadOnly]
# Por:
# permission_classes = [IsAdminOrVendedorOrReadOnly]
