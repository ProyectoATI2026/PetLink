from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    """
    Formulario personalizado para inicio de sesión.
    """
    username = forms.CharField(
        label=_("Nombre de Usuario"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Ingrese su usuario')
        })
    )
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Ingrese su contraseña')
        })
    )


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para el registro de nuevos usuarios en el sistema.
    """
    email = forms.EmailField(
        required=True,
        label=_("Correo Electrónico"),
        widget=forms.EmailInput(attrs={
            'placeholder': _('ejemplo@correo.com')
        })
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducción explícita de etiquetas para internacionalización
        if 'username' in self.fields:
            self.fields['username'].label = _("Nombre de Usuario")
        if 'password1' in self.fields:
            self.fields['password1'].label = _("Contraseña")
        if 'password2' in self.fields:
            self.fields['password2'].label = _("Confirmar Contraseña")