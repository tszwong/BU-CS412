# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
        class CreateProfileForm which inherits from forms.ModelForm
    """

    class Meta:
        """
            relates this form to the Profile model
        """
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_img']


class CreateStatusMessageForm(forms.ModelForm):
    """
        class CreateStatusMessageForm which inherits from forms.ModelForm
    """

    class Meta:
        """
            relates this form to the StatusMessage model
        """
        model = StatusMessage
        fields = ['message']


class UpdateProfileForm(forms.ModelForm):
    """
        Form for updating a profile
    """
    
    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_img']