# CÓDIGO COMPLETO PARA AGREGAR A gestion/views.py

# 1. AGREGAR ESTA CLASE DESPUÉS de IsAdminOrReadOnly (alrededor de la línea 40):

class IsAdminOrVendedorOrReadOnly(permissions.BasePermission):
    """
    Lectura para todos.
    Crear / actualizar para admin (is_staff=True) y vendedores (grupo Vendedor).
    Eliminar solo para admin.
    """
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


# 2. CAMBIAR en InmuebleViewSet (alrededor de la línea 80):
# Buscar:
#     permission_classes = [IsAdminOrReadOnly]
# Cambiar por:
#     permission_classes = [IsAdminOrVendedorOrReadOnly]

# 3. OPCIONAL: También cambiar VisitaViewSet si quieres que los vendedores gestionen visitas:
#     permission_classes = [IsAdminOrVendedorOrReadOnly]
