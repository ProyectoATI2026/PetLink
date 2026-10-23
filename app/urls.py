from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    PetRegisterView, 
    UserRegisterView, 
    UserProfileView, 
    UserProfileUpdateView,
    HomeView,
    AdoptionsView,
    MessagesView,
    AdminReportsView,
    ReportActionView,
    PetProfileUpdateView,
    PetProfileView,
    StartChatWithOwnerView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home_alias'),
    
    path('adoptions/', AdoptionsView.as_view(), name='adoptions'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('reports/', AdminReportsView.as_view(), name='reports'),
    path('api/reports/<int:report_id>/action/', ReportActionView.as_view(), name='report_action'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register_pet/', PetRegisterView.as_view(), name='register_pet'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('pet/<int:pk>/', PetProfileView.as_view(), name='pet_profile'),
    path('pet/<int:pk>/start-chat/', StartChatWithOwnerView.as_view(), name='start_chat'),
    path('pet/<int:pk>/edit/', PetProfileUpdateView.as_view(), name='pet_profile_edit'),
]
