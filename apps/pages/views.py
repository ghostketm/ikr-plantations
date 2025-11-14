from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import TemplateView
from apps.listings.models import Listing, Category
from apps.agents.models import Agent


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_listings'] = Listing.objects.filter(
            is_featured=True, is_published=True, status='available'
        )[:6]
        context['categories'] = Category.objects.all()[:8]
        context['featured_agents'] = Agent.objects.filter(
            verification_status='verified', is_featured=True
        )[:4]
        return context


def custom_404_view(request, exception):
    """Custom 404 error page with real estate humor."""
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """Custom 500 error page with real estate humor."""
    return render(request, '500.html', status=500)


def search_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return redirect('home')

    # Search listings
    listings = Listing.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(location__name__icontains=query) |
        Q(location__city__icontains=query) |
        Q(category__name__icontains=query),
        is_active=True,
        status='available'
    )[:10]  # Limit to 10 results

    # Search agents
    agents = Agent.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(agency_name__icontains=query) |
        Q(specialization__icontains=query),
        verification_status='verified'
    )[:10]  # Limit to 10 results

    # Search categories
    categories = Category.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:5]  # Limit to 5 results

    context = {
        'query': query,
        'listings': listings,
        'agents': agents,
        'categories': categories,
    }
    return render(request, 'search_results.html', context)


class LicensingView(TemplateView):
    template_name = 'pages/licensing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Real Estate Licensing - Kenya'
        return context


class TermsOfServiceView(TemplateView):
    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Terms of Service'
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy Policy'
        return context


class LegalDisclaimersView(TemplateView):
    template_name = 'pages/legal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Legal Disclaimers & Regulations'
        return context
