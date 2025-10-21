from django.urls import path
from . import views

urlpatterns = [
    path('<slug:listing_slug>/create/', views.inquiry_create, name='inquiry_create'),
    path('list/', views.inquiry_list, name='inquiry_list'),
    path('<int:pk>/', views.inquiry_detail, name='inquiry_detail'),
    path('<int:pk>/respond/', views.inquiry_respond, name='inquiry_respond'),
]
