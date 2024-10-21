# mini_fb/views.py

from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Image, Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

class ShowAllProfilesView(ListView):
    """
        Create a subclass of ListView to display all user profiles
    """
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    """
        Create a subclass of DetailView to display a single user
    """

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    """
        View to handle the creation of user profiles
    """
    
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'


class ProfileListView(ListView):
    """
        View to handle listing out profiles
    """
    model = Profile
    template_name = 'mini_fb/profile_list.html'
    context_object_name = 'profiles'
    

class CreateStatusMessageView(CreateView):
    """
        View to handle the creation of a status message
    """

    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self) -> str:
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})


    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        
        sm = form.save()
        print(f"StatusMessage created: {sm}") # for debug
        
        files = self.request.FILES.getlist('files')
        print(f"Files uploaded: {files}") # for debug
        
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()
            print(f"Image added: {image}") # for debug
        
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    

class UpdateProfileView(UpdateView):
    """
        View to handle updating a profile
    """
    
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'


    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context
    

class DeleteStatusMessageView(DeleteView):
    """
        View to handle deleting a status message
    """
    
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object
        return context
    

class UpdateStatusMessageView(UpdateView):
    """
        View to handle updating a status message.
    """
    
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'


    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object
        return context