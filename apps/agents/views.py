from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Agent, Rating
from .filters import AgentFilter
from apps.inquiries.models import Inquiry
from .forms import AgentCreationForm
from django.db import connection
from . import models
from apps.listings.forms import ListingForm # New import
from apps.listings.models import Listing # New import
from django.db.models import Avg, Q

def is_admin_or_staff(user):
    return user.is_superuser or user.is_staff

def is_agent(user):
    return hasattr(user, 'agent') and user.agent.is_active

def is_agent_or_admin_or_staff(user):
    return is_admin_or_staff(user) or is_agent(user)

@user_passes_test(is_admin_or_staff)
def create_agent(request):
    if request.method == 'POST':
        form = AgentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if hasattr(form, 'temp_password'):
                messages.success(request, f'New agent created successfully. Temporary password: {form.temp_password}')  # Note: In production, send email instead
            else:
                messages.success(request, 'User has been made an agent successfully.')
            return redirect('agents:agent_list')
    else:
        form = AgentCreationForm()
    return render(request, 'agents/create_agent.html', {'form': form})

def agent_list(request):
    agents = Agent.objects.filter(verification_status='verified').order_by('-rating')
    filter_form = AgentFilter(request.GET, queryset=agents)
    agents = filter_form.qs

    paginator = Paginator(agents, 12)  # 12 agents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'agents/agent_list.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
    })

@user_passes_test(is_agent_or_admin_or_staff)
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user # Assign the current user as the listing owner
            
            # If the user is an agent, assign the agent to the listing
            if hasattr(request.user, 'agent') and request.user.agent.is_active:
                listing.agent = request.user.agent
            else:
                # Admins/staff can create listings. If they need to assign an agent,
                # you'd add an 'agent' field to ListingForm for them.
                pass 
            listing.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('agents:agent_dashboard') # Redirect to agent dashboard or listing detail
    else:
        form = ListingForm()
    return render(request, 'agents/create_listing.html', {'form': form})

def agent_detail(request, pk):
    agent = get_object_or_404(Agent.objects.select_related('user__profile'), pk=pk, verification_status='verified')
    listings = agent.user.listings.filter(status='available')
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating:
            Rating.objects.update_or_create(
                agent=agent,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            # Recalculate agent's average rating using the imported Avg function
            agent.rating = agent.ratings.aggregate(Avg('rating'))['rating__avg']
            agent.save()
            messages.success(request, 'Your rating has been submitted.')
            return redirect('agents:agent_detail', pk=pk)
    return render(request, 'agents/agent_detail.html', {'agent': agent, 'listings': listings})


@login_required
def agent_dashboard(request):
    agent = None
    listings_qs = Listing.objects.none()
    inquiries_qs = Inquiry.objects.none()

    if request.user.is_superuser:
        listings_qs = Listing.objects.all()
        inquiries_qs = Inquiry.objects.all()
    elif hasattr(request.user, 'agent') and request.user.agent.is_active:
        agent = request.user.agent
        # Use prefetch_related for efficiency if you access related models in the template
        listings_qs = agent.user.listings.all().prefetch_related('inquiries')
        inquiries_qs = Inquiry.objects.filter(listing__agent=agent)
    else:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('pages:home')

    active_listings_count = listings_qs.filter(status='available').count()
    new_inquiries_count = inquiries_qs.filter(status='pending').count()
    
    # Order inquiries for consistent de-duplication
    ordered_inquiries = inquiries_qs.order_by('listing', 'user', 'subject', 'message', '-created_at')

    # Use performant DB-level distinct on PostgreSQL, fallback to Python for SQLite
    if connection.vendor == 'postgresql':
        inquiries = ordered_inquiries.distinct('listing', 'user', 'subject', 'message')
    else:
        # For SQLite and other DBs, de-duplicate in Python.
        seen_inquiries = set()
        unique_inquiries = []
        for inquiry in ordered_inquiries:
            inquiry_identifier = (inquiry.listing_id, inquiry.user_id, inquiry.subject, inquiry.message)
            if inquiry_identifier not in seen_inquiries:
                unique_inquiries.append(inquiry)
                seen_inquiries.add(inquiry_identifier)
        inquiries = unique_inquiries

    return render(request, 'agents/agent_dashboard.html', {
        'agent': agent,
        'listings': listings_qs,
        'active_listings_count': active_listings_count,
        'inquiries': inquiries,
        'new_inquiries_count': new_inquiries_count
    })

@user_passes_test(is_admin_or_staff)
def remove_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.is_active = False
        agent.save()
        messages.success(request, f'Agent {agent.user.get_full_name()} has been deactivated.')
        return redirect('agents:agent_list')
    return render(request, 'agents/remove_agent.html', {'agent': agent})
