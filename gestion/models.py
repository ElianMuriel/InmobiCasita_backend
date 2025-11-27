from django.db import models
from django.contrib.auth.models import User


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_rol


class Propietario(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Cliente(models.Model):
    TIPO_CLIENTE_CHOICES = (
        ('COMPRADOR', 'Comprador'),
        ('ARRENDATARIO', 'Arrendatario'),
        ('INVERSOR', 'Inversor'),
        ('OTRO', 'Otro'),
    )

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, default='COMPRADOR')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class TipoInmueble(models.Model):
    nombre_tipo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_tipo


class Inmueble(models.Model):
    TIPO_OPERACION_CHOICES = (
        ('VENTA', 'Venta'),
        ('ARRIENDO', 'Arriendo'),
        ('AMBOS', 'Venta y Arriendo'),
    )

    ESTADO_CHOICES = (
        ('DISPONIBLE', 'Disponible'),
        ('RESERVADO', 'Reservado'),
        ('VENDIDO', 'Vendido'),
        ('ARRENDADO', 'Arrendado'),
        ('INACTIVO', 'Inactivo'),
    )

    tipo = models.ForeignKey(TipoInmueble, on_delete=models.PROTECT, related_name='inmuebles')
    propietario = models.ForeignKey(Propietario, on_delete=models.PROTECT, related_name='inmuebles')
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inmuebles_registrados'
    )

    codigo_interno = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100, blank=True)

    tipo_operacion = models.CharField(max_length=20, choices=TIPO_OPERACION_CHOICES)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_arriendo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    numero_habitaciones = models.IntegerField(default=0)
    numero_banos = models.IntegerField(default=0)
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')

    def __str__(self):
        return f"{self.codigo_interno} - {self.titulo}"


class Visita(models.Model):
    ESTADO_CHOICES = (
        ('PROGRAMADA', 'Programada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    )

    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='visitas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='visitas')
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visitas_registradas'
    )

    fecha_hora = models.DateTimeField()
    comentarios = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PROGRAMADA')

    def __str__(self):
        return f"Visita {self.id} - {self.inmueble}"


class Contrato(models.Model):
    TIPO_CONTRATO_CHOICES = (
        ('VENTA', 'Venta'),
        ('ARRENDAMIENTO', 'Arrendamiento'),
    )

    ESTADO_CHOICES = (
        ('ACTIVO', 'Activo'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )

    inmueble = models.ForeignKey(Inmueble, on_delete=models.PROTECT, related_name='contratos')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='contratos')
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos_registrados'
    )

    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Contrato {self.id} - {self.inmueble}"


class Pago(models.Model):
    METODO_PAGO_CHOICES = (
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('TARJETA', 'Tarjeta'),
        ('OTRO', 'Otro'),
    )

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='EFECTIVO')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Pago {self.monto} - {self.fecha_pago}"
