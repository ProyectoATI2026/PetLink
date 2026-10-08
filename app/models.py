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