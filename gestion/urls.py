from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RolViewSet, PropietarioViewSet, ClienteViewSet,
    TipoInmuebleViewSet, InmuebleViewSet,
    VisitaViewSet, ContratoViewSet, PagoViewSet, ProfileView,
    register, mi_cliente, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'propietarios', PropietarioViewSet, basename='propietario')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'tipos-inmueble', TipoInmuebleViewSet, basename='tipo-inmueble')
router.register(r'inmuebles', InmuebleViewSet, basename='inmueble')
router.register(r'visitas', VisitaViewSet, basename='visita')
router.register(r'contratos', ContratoViewSet, basename='contrato')
router.register(r'pagos', PagoViewSet, basename='pago')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('auth/register/', register, name='register'),
    path('auth/mi-cliente/', mi_cliente, name='mi-cliente'),
]
