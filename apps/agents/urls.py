from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.agent_list, name='agent_list'),
    path('create/', views.create_agent, name='create_agent'),
    path('<int:pk>/', views.agent_detail, name='agent_detail'),
    path('<int:pk>/remove/', views.remove_agent, name='remove_agent'),
    path('dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('listings/create/', views.create_listing, name='create_listing'),
]
