from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm, AgentProfileForm
from .models import Profile


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def agent_profile_edit(request):
    if not hasattr(request.user, 'agent_profile'):
        messages.error(request, 'You are not an agent.')
        return redirect('profile')

    agent_profile = request.user.agent_profile
    if request.method == 'POST':
        form = AgentProfileForm(request.POST, instance=agent_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agent profile updated successfully.')
            return redirect('profile')
    else:
        form = AgentProfileForm(instance=agent_profile)
    return render(request, 'users/agent_profile_edit.html', {'form': form})
