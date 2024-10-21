# mini_fb/models.py

from django.db import models
from django.urls import reverse

class Profile(models.Model):
    """
        Encapsulate the idea of a Profile for a Facebook user.
    """
    
    # Data attributes of a Facebook user profile
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    profile_img = models.URLField(blank=False)

    def get_status_messages(self):
        """
            an accessor method to obtain all status messages for Profile
        """
        status_msgs = StatusMessage.objects.filter(article=self)
        return status_msgs
    
    
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.pk)])


    def __str__(self):
        """
            Return a string representation of this Profile object.
        """
        return f'{self.first_name} {self.last_name} from {self.city}'
    

class StatusMessage(models.Model):
    """
        Encapsulate the idea of a Status Message for a user.
    """

    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def get_images(self):
        """
            an accessor method to obtain all images for Profile
        """
        images = Image.objects.filter(status_message=self)
        return images

    def __str__(self):
        """
            Return a string representation of this StatusMessage object.
        """
        return f'Status by {self.profile.first_name} {self.profile.last_name} at {self.timestamp}: {self.message}'
    

class Image(models.Model):
    """
        Encapsulate the idea of an image file (not a URL) that is stored in the Django media directory
    """
    
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images') # one to many
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
            Return a string representation of this object
        """
        return f'Image for status: {self.status_message.message} uploaded at {self.timestamp}'
    