from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para el proyecto.
    Permite extender campos futuros si se requiere (ej. foto, teléfono, rol).
    """
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return self.username


class AuditLog(models.Model):
    """
    Modelo para registrar las acciones clave de seguridad y acceso en el sistema.
    """
    ACCIONES_CHOICES = [
        ('LOGIN_SUCCESS', _('Inicio de Sesión Exitoso')),
        ('LOGIN_FAILED', _('Intento de Login Fallido')),
        ('LOGOUT', _('Cierre de Sesión')),
        ('USER_REGISTERED', _('Registro de Usuario')),
    ]

    usuario = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Usuario')
    )
    accion = models.CharField(
        max_length=50,
        choices=ACCIONES_CHOICES,
        verbose_name=_('Acción')
    )
    direccion_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('Dirección IP')
    )
    detalles = models.TextField(
        blank=True,
        verbose_name=_('Detalles')
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha y Hora')
    )

    class Meta:
        verbose_name = _('Log de Auditoría')
        verbose_name_plural = _('Logs de Auditoría')
        ordering = ['-fecha_hora']

    def __str__(self):
        user_str = self.usuario.username if self.usuario else _('Anónimo')
        return f"{self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')} - {user_str} - {self.accion}"

class CustomPet(models.Model):
    """
    Modelo para representar una mascota en el sistema.
    """
    nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))
    especie = models.CharField(max_length=50, verbose_name=_('Especie'))
    raza = models.CharField(max_length=50, verbose_name=_('Raza / Mestizaje'), blank=True)
    edad = models.DateField(verbose_name=_('Edad'), null=True, blank=True)
    genero = models.CharField(max_length=10, verbose_name=_('Género'), blank=True)
    descripcion = models.TextField(verbose_name=_('Breve Descripción / Estado'), blank=True)
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True, verbose_name=_('Imagen de la Mascota'))
    
    propietario = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mascotas',
        verbose_name=_('Propietario')
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Registro'))

    class Meta:
        verbose_name = _('Mascota')
        verbose_name_plural = _('Mascotas')
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.especie})"