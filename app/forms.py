from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import CustomPet, CustomUser, UserProfile

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
    name = forms.CharField(
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

    birth_date = forms.DateField(
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

    description = forms.CharField(
        label=_("Breve Descripción / Estado"),
        widget=forms.Textarea(attrs={
            'placeholder': _('Ingrese una descripción de la mascota'),
            'rows': 4
        }),
        required=False
    )

    image = forms.ImageField(
        label=_("Imagen de la Mascota"),
        required=True
    )

    class Meta:
        model = CustomPet
        fields = ('name', 'species', 'breed', 'birth_date', 'gender', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducción explícita de etiquetas para internacionalización
        self.fields['name'].label = _("Nombre de la Mascota")
        self.fields['species'].label = _("Especie")
        self.fields['breed'].label = _("Raza / Mestizaje")
        self.fields['birth_date'].label = _("Edad")
        self.fields['gender'].label = _("Género")
        self.fields['description'].label = _("Breve Descripción / Estado")
        self.fields['image'].label = _("Foto de Perfil de la Mascota")

class CustomPetForm(forms.ModelForm):
    class Meta:
        model = CustomPet
        fields = ['name', 'species', 'breed', 'birth_date', 'gender', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre de la mascota')}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej. Perro, Gato')}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej. Mestizo, Poodle')}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Macho / Hembra')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Descripción...')}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'auth-form-group input'}),
            'last_name': forms.TextInput(attrs={'class': 'auth-form-group input'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['id_number', 'birth_date', 'gender', 'location', 'interests']
        widgets = {
            'id_number': forms.TextInput(attrs={'class': 'auth-form-group input'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'auth-form-group input'}),
            'gender': forms.Select(attrs={'class': 'auth-form-group input'}),
            'location': forms.TextInput(attrs={'class': 'auth-form-group input'}),
            'interests': forms.Textarea(attrs={'rows': 3, 'class': 'auth-form-group input'}),
        }