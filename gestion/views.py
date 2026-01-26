from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Rol, Propietario, Cliente, TipoInmueble,
    Inmueble, Visita, Contrato, Pago
)
from .serializers import (
    RolSerializer, PropietarioSerializer, ClienteSerializer,
    TipoInmuebleSerializer, InmuebleSerializer,
    VisitaSerializer, ContratoSerializer, PagoSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Lectura para todos.
    Crear / actualizar / eliminar solo para usuarios admin (is_staff=True).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre_rol']


class PropietarioViewSet(viewsets.ModelViewSet):
    queryset = Propietario.objects.all()
    serializer_class = PropietarioSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombres', 'apellidos', 'identificacion', 'ciudad']


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombres', 'apellidos', 'identificacion', 'ciudad', 'tipo_cliente']


class TipoInmuebleViewSet(viewsets.ModelViewSet):
    queryset = TipoInmueble.objects.all()
    serializer_class = TipoInmuebleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre_tipo']


class InmuebleViewSet(viewsets.ModelViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['codigo_interno', 'titulo', 'ciudad', 'barrio', 'tipo_operacion', 'estado']
       
    def get_queryset(self):
        queryset = Inmueble.objects.all()
        usuario = self.request.query_params.get('usuario', None)
        if usuario:
            queryset = queryset.filter(usuario_id=usuario)
        return queryset


class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['inmueble__codigo_interno', 'cliente__nombres', 'cliente__apellidos', 'estado']


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['tipo_contrato', 'estado', 'inmueble__codigo_interno', 'cliente__nombres', 'cliente__apellidos']


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['contrato__id', 'metodo_pago']


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mi_cliente(request):
    '''
    Obtiene el perfil de cliente asociado al usuario actual
    '''
    try:
        cliente = Cliente.objects.get(user=request.user)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    except Cliente.DoesNotExist:
        return Response(
            {'error': 'No se encontró perfil de cliente para este usuario'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registra un nuevo cliente y crea un usuario de Django
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        nombres = request.data.get('nombres')
        apellidos = request.data.get('apellidos')
        identificacion = request.data.get('identificacion')
        email = request.data.get('email')
        telefono = request.data.get('telefono', '')
        direccion = request.data.get('direccion', '')

        if not username or not password:
            return Response(
                {'error': 'Username y password son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'El usuario ya existe'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if email and User.objects.filter(email=email).exists():
            return Response(
                {'error': 'El email ya está registrado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email or '',
            first_name=nombres or '',
            last_name=apellidos or '',
            is_staff=False,
            is_active=True
        )

        cliente = Cliente.objects.create(
            nombres=nombres or '',
            apellidos=apellidos or '',
            identificacion=identificacion or '',
            email=email or '',
            telefono=telefono,
            direccion=direccion,
            activo=True,
            user=user
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'cliente_id': cliente.id,
            'message': 'Registro exitoso'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
