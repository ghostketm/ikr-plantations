from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('create/', views.listing_create, name='listing_create'),
    path('<slug:slug>/update/', views.listing_update, name='listing_update'),
    path('<slug:slug>/', views.listing_detail, name='listing_detail'),
]
