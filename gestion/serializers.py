from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rol, Propietario, Cliente, TipoInmueble, Inmueble, Visita, Contrato, Pago


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class PropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietario
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    crear_usuario = serializers.BooleanField(write_only=True, required=False, default=True)

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def create(self, validated_data):
        # Extraer el flag crear_usuario (no es un campo del modelo)
        crear_usuario = validated_data.pop('crear_usuario', True)
        
        # Si crear_usuario es True, crear el usuario automaticamente
        if crear_usuario:
            nombres = validated_data.get('nombres', '')
            identificacion = validated_data.get('identificacion', '')
            email = validated_data.get('email', '')
            
            # Verificar que tenga nombres e identificacion
            if not nombres or not identificacion:
                raise serializers.ValidationError(
                    'Se requieren nombres e identificacion para crear usuario automaticamente'
                )
            
            # Crear usuario con username = nombres e identificacion como contrasena
            username = nombres.replace(' ', '_').lower()[:30]  # Limitar a 30 caracteres
            
            # Verificar que el username no exista
            if User.objects.filter(username=username).exists():
                # Si ya existe, agregar un sufijo
                counter = 1
                original_username = username
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}_{counter}"
                    counter += 1
            
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                password=identificacion,
                email=email or '',
                first_name=nombres or '',
                is_staff=False,
                is_active=True
            )
            
            validated_data['user'] = user
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # No procesar crear_usuario en updates
        validated_data.pop('crear_usuario', None)
        return super().update(instance, validated_data)

    class Meta:
        model = Cliente
        fields = '__all__'


class TipoInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInmueble
        fields = '__all__'


class InmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inmueble
        fields = '__all__'


class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
