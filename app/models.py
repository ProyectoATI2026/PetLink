from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    ACTION_CHOICES = [
        ('LOGIN_SUCCESS', _('Inicio de Sesión Exitoso')),
        ('LOGIN_FAILED', _('Intento de Login Fallido')),
        ('LOGOUT', _('Cierre de Sesión')),
        ('USER_REGISTERED', _('Registro de Usuario')),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Usuario')
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name=_('Acción')
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('Dirección IP')
    )
    details = models.TextField(
        blank=True,
        verbose_name=_('Detalles')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha y Hora')
    )

    class Meta:
        verbose_name = _('Log de Auditoría')
        verbose_name_plural = _('Logs de Auditoría')
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.username if self.user else _('Anónimo')
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {user_str} - {self.action}"

class CustomPet(models.Model):
    """
    Modelo para representar una mascota en el sistema.
    """
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    species = models.CharField(max_length=50, verbose_name=_('Especie'))
    breed = models.CharField(max_length=50, verbose_name=_('Raza / Mestizaje'), blank=True)
    birth_date = models.DateField(verbose_name=_('Edad'), null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name=_('Género'), blank=True)
    description = models.TextField(verbose_name=_('Breve Descripción / Estado'), blank=True)
    image = models.ImageField(upload_to='mascotas/', null=True, blank=True, verbose_name=_('Imagen de la Mascota'))
    
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='pets',
        verbose_name=_('Propietario')
    )
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Registro'))

    class Meta:
        verbose_name = _('Mascota')
        verbose_name_plural = _('Mascotas')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.species})"

class UserProfile(models.Model):
    """
    Modelo de perfil extendido del usuario (relación uno a uno según mejores prácticas de DB).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Usuario')
    )
    id_number = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name=_('Cédula de identidad'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Fecha de nacimiento'))
    gender = models.CharField(
        max_length=20,
        choices=[('Masculino', _('Masculino')), ('Femenino', _('Femenino'))],
        null=True,
        blank=True,
        verbose_name=_('Género')
    )
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Ubicación'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Verificado'))
    interests = models.TextField(null=True, blank=True, help_text=_("Separados por comas o en formato adecuado"), verbose_name=_('Gustos / Preferencias'))
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name=_('Foto de Perfil'))

    class Meta:
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfiles')

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Alias para compatibilidad con develop
ProfileInfo = UserProfile

@receiver(post_save, sender=CustomUser)
def handle_user_profile_creation(sender, instance, created, **kwargs):
    """
    Buena práctica adoptada de develop:
    Crea automáticamente el perfil de usuario cuando se registra un nuevo CustomUser,
    o lo guarda si ya existe, evitando duplicados.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

class Pet(models.Model):
    # Relación de muchos a uno: un usuario puede tener varias mascotas
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50) # Raza y especie (ej: Golden Retriever)
    age = models.IntegerField() # Edad en años

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
