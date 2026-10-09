from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

# Importación de modelos y formularios propios
from .models import AuditLog, CustomPet, CustomUser # o Group/Profile según tu modelo
from .forms import CustomLoginForm, CustomPetCreationForm, CustomUserCreationForm

# -----------------------------------------------------------------------------
# HELPER / UTILIDAD DE AUDITORÍA
# -----------------------------------------------------------------------------
def registrar_log_auditoria(request, usuario, accion, detalles=""):
    """
    Función auxilar para registrar eventos de seguridad y acceso en la BD.
    """
    ip_cliente = request.META.get('REMOTE_ADDR', '0.0.0.0')
    AuditLog.objects.create(
        usuario=usuario if usuario.is_authenticated else None,
        accion=accion,
        direccion_ip=ip_cliente,
        detalles=detalles
    )


# -----------------------------------------------------------------------------
# 1. VISTAS DE AUTENTICACIÓN (LOGIN / LOGOUT)
# -----------------------------------------------------------------------------
class CustomLoginView(LoginView):
    """
    Gestiona el inicio de sesión del usuario.
    """
    template_name = 'login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Ejecuta la autenticación de Django
        response = super().form_valid(form)
        
        # Auditoría: Registrar ingreso exitoso
        registrar_log_auditoria(
            request=self.request,
            usuario=self.request.user,
            accion="LOGIN_SUCCESS",
            detalles=_("El usuario inició sesión correctamente.")
        )
        messages.success(self.request, _("¡Bienvenido de nuevo!"))
        return response

    def form_invalid(self, form):
        # Auditoría: Registrar intento fallido
        username_intentado = form.cleaned_data.get('username', 'Desconocido')
        registrar_log_auditoria(
            request=self.request,
            usuario=None,
            accion="LOGIN_FAILED",
            detalles=f"Intento fallido para el usuario: {username_intentado}"
        )
        messages.error(self.request, _("Nombre de usuario o contraseña incorrectos."))
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """
    Cierra la sesión activa del usuario.
    """
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            registrar_log_auditoria(
                request=request,
                usuario=request.user,
                accion="LOGOUT",
                detalles=_("El usuario cerró sesión.")
            )
        return super().dispatch(request, *args, **kwargs)


# -----------------------------------------------------------------------------
# 2. GESTIÓN DE USUARIOS Y ROLES
# -----------------------------------------------------------------------------
class RegistroUsuarioView(CreateView):
    """
    Permite registrar nuevos usuarios en el sistema.
    """
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Auditoría: Registro de nuevo usuario
        registrar_log_auditoria(
            request=self.request,
            usuario=self.object,
            accion="USER_REGISTERED",
            detalles=_("Nuevo usuario registrado en la plataforma.")
        )
        messages.success(self.request, _("Cuenta creada exitosamente. Ya puedes iniciar sesión."))
        return response


class ListaUsuariosView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Vista protegida solo para administradores/roles con permiso explícito.
    """
    model = CustomUser
    template_name = 'lista_usuarios.html'
    context_object_name = 'usuarios'
    permission_required = 'autenticacion.view_customuser' # Requisito de permiso


# -----------------------------------------------------------------------------
# 3. MÓDULO DE LOGS DE AUDITORÍA
# -----------------------------------------------------------------------------
class AuditLogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Muestra el historial/tabla de auditoría a los administradores.
    """
    model = AuditLog
    template_name = 'logs_auditoria.html'
    context_object_name = 'logs'
    paginate_by = 20 # Paginación
    permission_required = 'autenticacion.view_auditlog'

    def get_queryset(self):
        # Ordenar los logs del más reciente al más antiguo
        return AuditLog.objects.select_related('usuario').order_by('-fecha_hora')

# -----------------------------------------------------------------------------
# 4. MÓDULO DE REGISTRO MASCOTAS
# -----------------------------------------------------------------------------

class RegistroMascotaView(LoginRequiredMixin, CreateView):
    """
    Permite a los usuarios registrados agregar mascotas al sistema.
    """
    model = CustomPet  
    form_class = CustomPetCreationForm 
    template_name = 'register_pet.html'
    success_url = reverse_lazy('pet_list')  # Redirige a la lista de mascotas después del registro

    def form_valid(self, form):
        # Asignar el usuario actual como propietario de la mascota
        form.instance.propietario = self.request.user
        response = super().form_valid(form)
        
        # Auditoría: Registro de nueva mascota
        registrar_log_auditoria(
            request=self.request,
            usuario=self.request.user,
            accion="MASCOTA_REGISTERED",
            detalles=f"Se registró una nueva mascota: {form.instance.nombre}"
        )
        messages.success(self.request, _("Mascota registrada exitosamente."))
        return response