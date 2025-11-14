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
from django.db.models import Avg

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
            return redirect('agents_agent_list')
    else:
        form = AgentCreationForm()
    return render(request, 'agents/create_agent.html', {'form': form})

def agent_list(request):
    agents = Agent.objects.all().order_by('verification_status', '-rating')
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
            return redirect('agents_agent_dashboard') # Redirect to agent dashboard or listing detail
    else:
        form = ListingForm()
    return render(request, 'agents/create_listing.html', {'form': form})

def agent_detail(request, pk):
    agent = get_object_or_404(Agent, pk=pk, verification_status='verified')
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
            return redirect('agents_agent_detail', pk=pk)
    return render(request, 'agents/agent_detail.html', {'agent': agent, 'listings': listings})


@login_required
def agent_dashboard(request):
    if request.user.is_superuser:
        # Super admin can access dashboard
        agent = None
        listings = Listing.objects.all()
        active_listings_count = listings.filter(status='available').count()
        all_inquiries_queryset = Inquiry.objects.all().order_by('-created_at')
    elif hasattr(request.user, 'agent') and request.user.agent.is_active:
        agent = request.user.agent
        listings = request.user.listings.all()
        active_listings_count = listings.filter(status='available').count()
        all_inquiries_queryset = Inquiry.objects.filter(listing__agent=request.user.agent).order_by('-created_at')
    else:
        return redirect('agents_create_agent')

    # Use performant DB-level distinct on PostgreSQL, fallback to Python for SQLite
    if connection.vendor == 'postgresql':
        # For PostgreSQL, distinct on specific fields is highly efficient.
        # We order by the fields we want to be distinct on, plus -created_at to get the latest.
        inquiries = all_inquiries_queryset.order_by('listing', 'user', 'subject', 'message', '-created_at').distinct('listing', 'user', 'subject', 'message')
    else:
        # For SQLite and other DBs, de-duplicate in Python.
        seen_inquiries = set()
        unique_inquiries = []
        for inquiry in all_inquiries_queryset:
            # Create a unique identifier for what is considered a "duplicate"
            inquiry_identifier = (inquiry.listing_id, inquiry.user_id, inquiry.subject, inquiry.message)
            if inquiry_identifier not in seen_inquiries:
                unique_inquiries.append(inquiry)
                seen_inquiries.add(inquiry_identifier)
        inquiries = unique_inquiries

    new_inquiries_count = sum(1 for i in inquiries if i.status == 'pending')

    return render(request, 'agents/agent_dashboard.html', {
        'agent': agent,
        'listings': listings,
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
        return redirect('agents_agent_list')
    return render(request, 'agents/remove_agent.html', {'agent': agent})
