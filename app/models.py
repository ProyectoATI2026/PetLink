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
    
class Publication(models.Model):
    """
    Represents a publication created by a user in PetLink.
    """

    class PublicationType(models.TextChoices):
        GENERAL = 'GENERAL', _('General')
        ADOPTION = 'ADOPTION', _('Adoption')
        LOST = 'LOST', _('Lost Pet')
    

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_('Author')
    )

    pet = models.ForeignKey(
        CustomPet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='publications',
        verbose_name=_('Pet')
    )

    publication_type = models.CharField(
        max_length=20,
        choices=PublicationType.choices,
        default=PublicationType.GENERAL,
        verbose_name=_('Publication Type')
    )
    
    title = models.CharField(
        max_length = 200,
        verbose_name=_('Title')
    )

    description = models.TextField(
        verbose_name=_('Description')
    )

    image = models.ImageField(
        upload_to='publications/',
        null=True,
        blank=True,
        verbose_name=_('Image')
    )

    location = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Location')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )

    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.get_publication_type_display()}"

class Comment(models.Model):
    """Represents a comment made by a user on a publication,
       Comments can also be replies yo other comments.
    """
    
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Publication')
    )
    
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Author')
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name=_('Parent Comment')
    )
    
    contet = models.TextField (
        verbose_name=_('Content')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username}"

class AdoptionRequest(models.Model):
    """
    Represents a request made by a user to adopt a pet
    through an adoption publication.
    """

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        REJECTED = 'REJECTED', _('Rejected')
        CANCELLED = 'CANCELLED', _('Cancelled')
        COMPLETED = 'COMPLETED', _('Completed')

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name='adoption_requests',
        verbose_name=_('Publication')
    )

    applicant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='adoption_requests',
        verbose_name=_('Applicant')
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Status')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Adoption Request')
        verbose_name_plural = _('Adoption Requests')
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['publication', 'applicant'],
                name='unique_adoption_request'
            )
        ]

    def __str__(self):
        return f"{self.applicant.username} - {self.publication.title}"

class Conversation(models.Model):
    """
    Represents a conversation between PetLink users.
    It can optionally originate from an adoption request.
    """

    participants = models.ManyToManyField(
        CustomUser,
        related_name='conversations',
        verbose_name=_('Participants')
    )

    adoption_request = models.OneToOneField(
        AdoptionRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversation',
        verbose_name=_('Adoption Request')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    """
    Represents a message sent inside a conversation.
    """

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Conversation')
    )

    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('Sender')
    )

    content = models.TextField(
        verbose_name=_('Content')
    )

    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Sent At')
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Read')
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.username}"

class Rating(models.Model):
    """
    Represents a rating given by one user to another
    after an adoption process.
    """

    adoption_request = models.ForeignKey(
        AdoptionRequest,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name=_('Adoption Request')
    )

    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ratings_given',
        verbose_name=_('Reviewer')
    )

    reviewed_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ratings_received',
        verbose_name=_('Reviewed User')
    )

    score = models.PositiveSmallIntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        verbose_name=_('Score')
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['adoption_request', 'reviewer'],
                name='unique_rating_per_reviewer'
            )
        ]

    def __str__(self):
        return f"{self.reviewer.username} -> {self.reviewed_user.username}: {self.score}"

class Report(models.Model):
    """
    Represents a report submitted by a user against
    a publication, comment or user account.
    """

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        RESOLVED = 'RESOLVED', _('Resolved')
        DISMISSED = 'DISMISSED', _('Dismissed')

    reporter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reports_submitted',
        verbose_name=_('Reporter')
    )

    reported_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports_received',
        verbose_name=_('Reported User')
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name=_('Publication')
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name=_('Comment')
    )

    reason = models.TextField(
        verbose_name=_('Reason')
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Status')
    )

    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed',
        verbose_name=_('Reviewed By')
    )

    resolution_notes = models.TextField(
        blank=True,
        verbose_name=_('Resolution Notes')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Resolved At')
    )

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ['-created_at']

    def __str__(self):
        return f"Report #{self.id} - {self.status}"

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
