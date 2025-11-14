from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from .forms import InquiryForm
from apps.listings.models import Listing


@login_required
def inquiry_create(request, listing_slug):
    listing = get_object_or_404(Listing, slug=listing_slug, is_active=True)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.listing = listing
            inquiry.user = request.user
            inquiry.save()

            # Send confirmation email to customer
            subject_customer = f'Inquiry Sent for {listing.title}'
            message_customer = f'''
            Dear {request.user.get_full_name()},

            Your inquiry for "{listing.title}" has been sent successfully.

            Subject: {inquiry.subject}
            Message: {inquiry.message}

            The agent will respond to you soon.

            Best regards,
            Your Real Estate Team
            '''
            send_mail(
                subject_customer,
                message_customer,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True
            )

            # Send email notification to agent
            subject = f'New Inquiry for {listing.title}'
            message = f'''
            You have received a new inquiry for your listing "{listing.title}".

            From: {request.user.email}
            Subject: {inquiry.subject}
            Message: {inquiry.message}

            Please log in to your dashboard to respond.
            '''
            email_to_agent = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [listing.agent.user.email],
                reply_to=[request.user.email],
            )
            email_to_agent.send(fail_silently=True)

            messages.success(request, 'Your inquiry has been sent successfully. You will receive a confirmation email.')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = InquiryForm()
    return render(request, 'inquiries/inquiry_form.html', {
        'form': form,
        'listing': listing
    })


@login_required
def inquiry_list(request):
    inquiries = request.user.inquiries.all().order_by('-created_at')
    return render(request, 'inquiries/inquiry_list.html', {'inquiries': inquiries})


@login_required
def inquiry_detail(request, pk):
    inquiry = get_object_or_404(request.user.inquiries, pk=pk)
    return render(request, 'inquiries/inquiry_detail.html', {'inquiry': inquiry})


@login_required
def inquiry_respond(request, pk):
    inquiry = get_object_or_404(request.user.agent.inquiries, pk=pk)
    if request.method == 'POST':
        response = request.POST.get('response')
        inquiry.response = response
        inquiry.responded_at = timezone.now()
        inquiry.status = 'responded'
        inquiry.save()

        # Send email to inquirer
        subject = f'Response to your inquiry for {inquiry.listing.title}'
        message = f'''
        Dear {inquiry.user.get_full_name()},

        You have received a response to your inquiry for "{inquiry.listing.title}".

        Your message: {inquiry.message}

        Agent's response: {inquiry.response}

        Best regards,
        {inquiry.listing.agent.get_full_name()}
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [inquiry.user.email],
            fail_silently=True
        )

        messages.success(request, 'Response sent successfully.')
        return redirect('inquiry_detail', pk=pk)
    return render(request, 'inquiries/inquiry_respond.html', {'inquiry': inquiry})
