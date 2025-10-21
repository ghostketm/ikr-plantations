from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search_view, name='search'),
    path('404/', views.custom_404_view, name='404'),
    path('500/', views.custom_500_view, name='500'),
]
