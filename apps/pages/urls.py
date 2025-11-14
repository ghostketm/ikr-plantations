from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search_view, name='search'),
    path('404/', views.custom_404_view, name='404'),
    path('500/', views.custom_500_view, name='500'),
    path('licensing/', views.LicensingView.as_view(), name='licensing'),
    path('terms/', views.TermsOfServiceView.as_view(), name='terms'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('legal/', views.LegalDisclaimersView.as_view(), name='legal'),
]
