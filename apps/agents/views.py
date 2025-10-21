from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import AgentProfile
from .filters import AgentFilter
from apps.inquiries.models import Inquiry


def agent_list(request):
    agents = AgentProfile.objects.filter(verification_status='verified').order_by('-rating')
    filter_form = AgentFilter(request.GET, queryset=agents)
    agents = filter_form.qs

    paginator = Paginator(agents, 12)  # 12 agents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'agents/agent_list.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
    })


def agent_detail(request, pk):
    agent = get_object_or_404(AgentProfile, pk=pk, verification_status='verified')
    listings = agent.user.listings.filter(status='available')
    return render(request, 'agents/agent_detail.html', {'agent': agent, 'listings': listings})


@login_required
def agent_dashboard(request):
    if not hasattr(request.user, 'agent_profile'):
        return redirect('agents_create_profile')
    profile = request.user.agent_profile
    listings = request.user.listings.all()
    active_listings_count = listings.filter(status='available').count()
    inquiries = Inquiry.objects.filter(listing__agent=request.user).order_by('-created_at')
    new_inquiries_count = inquiries.filter(status='pending').count()
    return render(request, 'agents/agent_dashboard.html', {
        'profile': profile,
        'listings': listings,
        'active_listings_count': active_listings_count,
        'inquiries': inquiries,
        'new_inquiries_count': new_inquiries_count
    })
