from django.urls import path
from . import views

urlpatterns = [
    path('', views.agent_list, name='agents_agent_list'),
    path('create/', views.create_agent, name='agents_create_agent'),
    path('<int:pk>/', views.agent_detail, name='agents_agent_detail'),
    path('<int:pk>/remove/', views.remove_agent, name='agents_remove_agent'),
    path('dashboard/', views.agent_dashboard, name='agents_agent_dashboard'),
    path('listings/create/', views.create_listing, name='agents_create_listing'), # New URL
]
