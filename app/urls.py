from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegistroMascotaView, RegistroUsuarioView, PerfilUsuarioView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('profile/', PerfilUsuarioView.as_view(), name='profile'),
    path('registro_mascota/', RegistroMascotaView.as_view(), name='registro_mascota'),
]