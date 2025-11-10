from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Listing, Category, Location, ListingImage
from .forms import ListingForm, ListingSearchForm
from .filters import ListingFilter


def listing_list(request):
    listings = Listing.objects.filter(is_active=True, status='available').order_by('-created_at')
    filter_form = ListingFilter(request.GET, queryset=listings)
    listings = filter_form.qs

    paginator = Paginator(listings, 12)  # 12 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    locations = Location.objects.all()

    return render(request, 'listings/listing_list.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'categories': categories,
        'locations': locations,
    })


def listing_detail(request, slug):
    listing = get_object_or_404(Listing, slug=slug, is_active=True)
    listing.views_count += 1
    listing.save(update_fields=['views_count'])

    related_listings = Listing.objects.filter(
        category=listing.category,
        is_active=True,
        status='available'
    ).exclude(id=listing.id)[:4]

    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'related_listings': related_listings,
    })


@login_required
def listing_create(request):
    if not hasattr(request.user, 'agent_profile'):
        messages.error(request, 'Only agents can create listings.')
        return redirect('profile')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.agent = request.user
            listing.save()

            # Handle image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm()
    return render(request, 'listings/listing_form.html', {'form': form})


@login_required
def listing_update(request, slug):
    listing = get_object_or_404(Listing, slug=slug, agent=request.user)
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
