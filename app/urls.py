from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegistroUsuarioView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
]