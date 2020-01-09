# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404

from django.http import Http404
from django.http import HttpResponse

from .models import Profile
from .forms import EditProfileForm

from .ws2812b import send_profile

def home(request):
    profiles = Profile.objects.all()
    return render(request, 'home.html', {'profiles': profiles})

def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            edited_profile = form.save(commit=False)
            edited_profile.save()
    else:
        form = EditProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'profile': profile, 'form': form})

def apply_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    
    print('Applying profile...')
    send_profile(profile)
    
    return redirect('edit_profile', pk=pk)