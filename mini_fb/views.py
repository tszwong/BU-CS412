# mini_fb/views.py

from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    """
        Create a subclass of ListView to display all user profiles
    """
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
