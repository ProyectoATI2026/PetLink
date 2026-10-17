from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from .models import AuditLog, CustomPet, CustomUser, UserProfile
from .forms import (
    CustomLoginForm,
    CustomUserCreationForm,
    CustomPetCreationForm,
    CustomPetForm,
    UserForm,
    UserProfileForm,
)

def register_audit_log(request, user, action, details=""):
    """
    Función auxiliar para registrar eventos de seguridad y acceso en la BD.
    """
    client_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    AuditLog.objects.create(
        user=user if (user and user.is_authenticated) else None,
        action=action,
        ip_address=client_ip,
        details=details
    )

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse_lazy('reports')
        return reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        register_audit_log(
            request=self.request,
            user=self.request.user,
            action="LOGIN_SUCCESS",
            details=_("El usuario inició sesión correctamente.")
        )
        messages.success(self.request, _("¡Bienvenido de nuevo!"))
        return response

    def form_invalid(self, form):
        attempted_username = form.cleaned_data.get('username', 'Desconocido')
        register_audit_log(
            request=self.request,
            user=None,
            action="LOGIN_FAILED",
            details=f"Intento fallido para el usuario: {attempted_username}"
        )
        messages.error(self.request, _("Nombre de usuario o contraseña incorrectos."))
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            register_audit_log(
                request=request,
                user=request.user,
                action="LOGOUT",
                details=_("El usuario cerró sesión.")
            )
        return super().dispatch(request, *args, **kwargs)

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Auditoría: Registro de nuevo usuario
        register_audit_log(
            request=self.request,
            user=self.object,
            action="USER_REGISTERED",
            details=_("Nuevo usuario registrado en la plataforma.")
        )
        messages.success(self.request, _("Cuenta creada exitosamente. Ya puedes iniciar sesión."))
        return response


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'
    permission_required = 'app.view_customuser'

class AuditLogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Muestra el historial/tabla de auditoría a los administradores.
    """
    model = AuditLog
    template_name = 'audit_logs.html'
    context_object_name = 'logs'
    paginate_by = 20
    permission_required = 'app.view_auditlog'

    def get_queryset(self):
        return AuditLog.objects.select_related('user').order_by('-timestamp')

class PetRegisterView(LoginRequiredMixin, CreateView):
    model = CustomPet  
    form_class = CustomPetCreationForm 
    template_name = 'register_pet.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        register_audit_log(
            request=self.request,
            user=self.request.user,
            action="PET_REGISTERED",
            details=f"Se registró una nueva mascota: {form.instance.name}"
        )
        messages.success(self.request, _("Mascota registrada exitosamente."))
        return response


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'id_number': f'V-{self.request.user.id:08d}',
                'birth_date': '2000-01-01',
                'gender': 'No especificado',
                'location': 'Caracas',
                'interests': 'Perros, Gatos, Adopción responsable',
                'is_verified': True
            }
        )
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = self.request.user.pets.all()
        
        interests_str = self.object.interests
        context['interests_list'] = [i.strip() for i in interests_str.split(',')] if interests_str else []
        
        return context

class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profile_edit.html'

    def get(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

class PetProfileView(LoginRequiredMixin, DetailView):
    model = CustomPet
    template_name = 'pet_profile.html'
    context_object_name = 'pet'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Permite verificar en la plantilla si el usuario actual es el propietario de la mascota
        context['is_owner'] = (self.object.owner == self.request.user)
        context['title'] = f"{self.object.name} - PetLink"
        return context


class PetProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'pet_profile_edit.html'

    def get(self, request, pk, *args, **kwargs):
        pet = get_object_or_404(CustomPet, pk=pk)
        
        # Control de permisos: solo el propietario puede editar a su mascota
        if pet.owner != request.user and not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, _("No tienes permiso para editar el perfil de esta mascota."))
            return redirect('pet_profile', pk=pet.pk)

        pet_form = CustomPetForm(instance=pet)
        context = {
            'pet': pet,
            'pet_form': pet_form,
            'title': f"Editar {pet.name} - PetLink",
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        pet = get_object_or_404(CustomPet, pk=pk)
        
        if pet.owner != request.user and not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, _("No tienes permiso para editar el perfil de esta mascota."))
            return redirect('pet_profile', pk=pet.pk)

        pet_form = CustomPetForm(request.POST, request.FILES, instance=pet)

        if pet_form.is_valid():
            pet_form.save()
            register_audit_log(
                request=request,
                user=request.user,
                action="PET_UPDATED",
                details=f"Perfil actualizado para la mascota ID #{pet.id}: {pet.name}"
            )
            messages.success(request, _("Perfil de la mascota actualizado correctamente."))
            return redirect('pet_profile', pk=pet.pk)

        context = {
            'pet': pet,
            'pet_form': pet_form,
            'title': f"Editar {pet.name} - PetLink",
        }
        return render(request, self.template_name, context)

class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect('reports')

        quick_filters = {
            'perros': CustomPet.objects.filter(species__iexact='perro').count(),
            'gatos': CustomPet.objects.filter(species__iexact='gato').count(),
            'aves': CustomPet.objects.filter(species__iexact='ave').count(),
            'otros': CustomPet.objects.exclude(species__iexact='perro').exclude(species__iexact='gato').exclude(species__iexact='ave').count(),
            'urgentes': 0
        }

        db_pets = CustomPet.objects.select_related('owner').all().order_by('-registration_date')[:4]

        posts = []

        context = {
            'posts': posts,
            'quick_filters': quick_filters,
            'featured_pets': db_pets,
            'active_tab': 'home',
            'title': 'Inicio - PetLink',
        }
        return render(request, self.template_name, context)

class AdoptionsView(View):
    template_name = 'adoptions.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect('reports')

        search_query = request.GET.get('q', '').strip()
        species_filter = request.GET.get('especie', '').strip()

        pets_qs = CustomPet.objects.select_related('owner').all().order_by('-registration_date')

        if search_query:
            pets_qs = pets_qs.filter(
                Q(name__icontains=search_query) |
                Q(breed__icontains=search_query) |
                Q(species__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if species_filter and species_filter.lower() != 'todos':
            pets_qs = pets_qs.filter(species__iexact=species_filter)

        context = {
            'pets': pets_qs,
            'total_pets': pets_qs.count(),
            'current_search': search_query,
            'current_species': species_filter if species_filter else 'todos',
            'active_tab': 'adoptions',
            'title': 'Adopciones - PetLink',
        }
        return render(request, self.template_name, context)


class MessagesView(LoginRequiredMixin, View):
    template_name = 'messages.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect('reports')

        conversations = []
        active_chat = None

        context = {
            'conversations': conversations,
            'active_chat': active_chat,
            'active_tab': 'messages',
            'title': 'Mensajes - PetLink',
        }
        return render(request, self.template_name, context)

class AdminReportsView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'reports.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("Acceso denegado: Se requieren credenciales de Administrador para ver la pantalla de moderación de reportes.")
        )
        return redirect('home')

    def get(self, request, *args, **kwargs):
        reports = []

        register_audit_log(
            request=request,
            user=request.user,
            action="ADMIN_ACCESS_REPORTS",
            details=_("El administrador accedió a la pantalla de moderación de reportes.")
        )

        context = {
            'reports': reports,
            'total_reports': len(reports),
            'active_tab': 'reports',
            'title': 'Moderación de Reportes - PetLink Admin',
        }
        return render(request, self.template_name, context)


class ReportActionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, report_id, *args, **kwargs):
        action = request.POST.get('accion', 'ignorar')
        reason = request.POST.get('motivo', 'Moderación estándar')

        audit_action = "POST_ELIMINADO" if action == 'eliminar' else "REPORTE_IGNORADO"
        details = f"El admin moderó el reporte #{report_id}: acción='{action}'. Motivo: {reason}"

        register_audit_log(
            request=request,
            user=request.user,
            action=audit_action,
            details=details
        )

        message = (
            f"El post asociado al reporte #{report_id} ha sido eliminado satisfactoriamente." 
            if action == 'eliminar' 
            else f"El reporte #{report_id} ha sido desestimado e ignorado."
        )

        return JsonResponse({
            'success': True,
            'report_id': report_id,
            'action': action,
            'message': message
        })
