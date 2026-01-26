# CAMBIOS PARA: gestion/views.py
# 
# INSTRUCCIONES:
# 1. Abrir el archivo: /opt/inmobicasita/gestion/views.py
# 2. Buscar la clase CustomTokenObtainPairSerializer
# 3. Buscar esta línea dentro del método get_token:
#    token['is_vendedor'] = bool(Inmueble.objects.filter(usuario=user).exists())
# 4. Reemplazarla por:
#    token['is_vendedor'] = bool(user.groups.filter(name='Vendedor').exists())
# 5. Asegurarse de que el import esté al inicio del archivo:
#    from django.contrib.auth.models import Group
#    (Si no está, agregarlo junto con los otros imports)

# EJEMPLO DE CÓDIGO COMPLETO:

"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group  # ← Agregar este import si no está

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            token['username'] = str(user.username)
            token['is_staff'] = bool(user.is_staff)
            token['user_id'] = int(user.id)
            
            # CAMBIO AQUÍ:
            # ANTES:
            # token['is_vendedor'] = bool(Inmueble.objects.filter(usuario=user).exists())
            # DESPUÉS:
            token['is_vendedor'] = bool(user.groups.filter(name='Vendedor').exists())
            
            try:
                cliente_profile = Cliente.objects.get(user=user)
                token['is_cliente'] = True
                token['cliente_id'] = int(cliente_profile.id)
            except Cliente.DoesNotExist:
                token['is_cliente'] = False
                token['cliente_id'] = None
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error adding custom claims for user {user.username}: {e}")
            token['is_vendedor'] = False
            token['is_cliente'] = False
            token['cliente_id'] = None
        return token
"""
