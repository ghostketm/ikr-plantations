from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Listing, Category, ListingImage
from .forms import ListingForm #, ListingSearchForm
from .filters import ListingFilter


def listing_list(request):
    listings = Listing.objects.filter(is_published=True, status='available').order_by('-created_at')
    filter_form = ListingFilter(request.GET, queryset=listings)
    listings = filter_form.qs

    paginator = Paginator(listings, 12)  # 12 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    # locations = Location.objects.all()

    return render(request, 'listings/listing_list.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'categories': categories,
        # 'locations': locations,
    })


def listing_detail(request, slug):
    listing = get_object_or_404(Listing, slug=slug, is_published=True)
    # listing.views_count += 1
    # listing.save(update_fields=['views_count'])

    related_listings = Listing.objects.filter(
        category=listing.category,
        is_published=True,
        status='available'
    ).exclude(id=listing.id)[:4]

    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'related_listings': related_listings,
    })


@login_required
def listing_create(request):
    # Allow admins (staff or superuser) or active and verified agents
    is_admin = request.user.is_staff or request.user.is_superuser
    is_active_verified_agent = (
        hasattr(request.user, 'agent') and
        request.user.agent.is_active and
        request.user.agent.verification_status == 'verified'
    )
    if not (is_admin or is_active_verified_agent):
        messages.error(request, 'Only active and verified agents or admins can create listings.')
        return redirect('profile')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            # The agent field expects an Agent instance, not a User instance.
            if hasattr(request.user, 'agent'):
                listing.agent = request.user.agent
            # The user field is not set, but the model requires it. Let's set it.
            listing.user = request.user
            # If the creator is an admin or a verified active agent, publish immediately
            if is_admin or is_active_verified_agent:
                listing.is_published = True
                listing.status = listing.status or 'available'
            listing.save()

            # Handle image uploads (support multiple files)
            images = request.FILES.getlist('images')
            for idx, image in enumerate(images):
                ListingImage.objects.create(listing=listing, image=image, is_main=(idx == 0))

            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm()
    return render(request, 'listings/listing_form.html', {'form': form})


@login_required
def listing_update(request, slug):
    listing = get_object_or_404(Listing, slug=slug)

    # Authorization: superusers/staff can edit any listing; agents can edit only their own listings
    if not (request.user.is_staff or request.user.is_superuser):
        if not hasattr(request.user, 'agent') or listing.agent != request.user.agent:
            messages.error(request, 'You do not have permission to edit this listing.')
            return redirect('listing_detail', slug=slug)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            listing = form.save()

            # Handle new image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form, 'listing': listing})
