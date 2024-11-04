# mini_fb/views.py

from django import forms
import django
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from .models import Friend, Image, Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm


class ShowAllProfilesView(ListView):
    """
        Create a subclass of ListView to display all user profiles
    """
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)


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


    def get_context_data(self, **kwargs):
        # Manually create context to avoid issues with self.object
        context = kwargs
        context['user_form'] = UserCreationForm()
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserCreationForm(request.POST)
        profile_form = self.get_form()

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect(self.success_url)
        else:
            # If the form is invalid, pass both forms to context for re-rendering
            return self.render_to_response(self.get_context_data(form=profile_form, user_form=user_form))

    def form_valid(self, form):
        # Only save form instance if user_form is also valid
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

class ProfileListView(ListView):
    """
        View to handle listing out profiles
    """
    model = Profile
    template_name = 'mini_fb/profile_list.html'
    context_object_name = 'profiles'
    

class CreateStatusMessageView(LoginRequiredMixin,CreateView):
    """
        View to handle the creation of a status message
    """

    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    login_url = reverse_lazy('login')


    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})


    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
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
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
        View to handle updating a profile
    """
    
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    login_url = reverse_lazy('login')


    def get_object(self):
        return Profile.objects.get(user=self.request.user)


    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context
    

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """
        View to handle deleting a status message
    """
    
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    login_url = reverse_lazy('login')

    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object
        return context
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """
        View to handle updating a status message.
    """
    
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    login_url = reverse_lazy('login')


    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object
        return context
    

class CreateFriendView(LoginRequiredMixin, django.views.generic.View):
    """
        View to handle adding a friend to a profile
    """

    login_url = reverse_lazy('login')

    
    def dispatch(self, request, *args, **kwargs):
        """
            read the URL parameters (from self.kwargs), use the object manager to find the 
            requisite Profile objects, and then call the Profile's add_friend method
            Finally, we can redirect the user back to the profile page
        """

        profile = Profile.objects.get(user=self.request.user)
        friend_profile = Profile.objects.get(pk=kwargs['other_pk'])
        profile.add_friend(friend_profile)
        return redirect('show_profile', pk=profile.pk)
        

class ShowFriendSuggestionsView(DetailView):
    """
        View to handle showing friend suggestions
    """
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'


    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        friends = Friend.objects.filter(profile1=profile).values_list('profile2', flat=True)
        reverse_friends = Friend.objects.filter(profile2=profile).values_list('profile1', flat=True)
        all_friend_ids = list(friends) + list(reverse_friends)
        friend_suggestions = Profile.objects.exclude(id__in=all_friend_ids).exclude(id=profile.id)
        context['friend_suggestions'] = friend_suggestions
        return context
    

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """
        View to handle showing the news feed
    """

    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'


    def get_object(self):
        return Profile.objects.get(user=self.request.user)
