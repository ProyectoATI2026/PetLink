from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomPet, CustomUser

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

class CustomPetCreationForm(forms.ModelForm):
    """
    Formulario para el registro de nuevas mascotas en el sistema.
    """
    petname = forms.CharField(
        required=True,
        label=_("Nombre de la Mascota"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Ingrese el nombre de la mascota')
        })
    )

    species = forms.CharField(
        required=True,
        label=_("Especie"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Ingrese la especie de la mascota')
        })
    )

    age = forms.DateField(
        label=_("Edad"),
        widget=forms.DateInput(attrs={
            'placeholder': _('Ingrese la edad de la mascota'),
            'type': 'date'
        })
    )

    breed = forms.CharField(
        label=_("Raza / Mestizaje"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Ingrese la raza de la mascota')
        })
    )

    gender = forms.ChoiceField(
        choices=[('M', _('Macho')), ('F', _('Hembra'))],
        label=_("Género"),
    )

    desc = forms.CharField(
        label=_("Breve Descripción / Estado"),
        widget=forms.Textarea(attrs={
            'placeholder': _('Ingrese una descripción de la mascota'),
            'rows': 4
        }),
        required=False
    )

    imagen = forms.ImageField(
        label=_("Imagen de la Mascota"),
        required=True
    )

    class Meta:
        model = CustomPet
        fields = ('petname', 'species', 'breed', 'age', 'gender', 'desc', 'imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducción explícita de etiquetas para internacionalización
        self.fields['petname'].label = _("Nombre de la Mascota")
        self.fields['species'].label = _("Especie")
        self.fields['breed'].label = _("Raza / Mestizaje")
        self.fields['age'].label = _("Edad")
        self.fields['gender'].label = _("Género")
        self.fields['desc'].label = _("Breve Descripción / Estado")
        self.fields['imagen'].label = _("Foto de Perfil de la Mascota")