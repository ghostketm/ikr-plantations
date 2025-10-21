from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('agent-profile/edit/', views.agent_profile_edit, name='agent_profile_edit'),
]
