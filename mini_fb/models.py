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


    def get_friends(self):
        """
            an accessor method to obtain all friends for Profile
        """
        f1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        f2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = list(f1) + list(f2)
        friend_profiles = Profile.objects.filter(id__in=friend_ids)
        return list(friend_profiles)

    
    def add_friend(self, other):
        """
            method to add friends for user
        """
        if self != other:
            if not Friend.objects.filter(profile1=self, profile2=other).exists() and \
                not Friend.objects.filter(profile1=other, profile2=self).exists():
                Friend.objects.create(profile1=self, profile2=other)


    def get_friend_suggestions(self):
        """
            an accessor method to obtain friend suggestions for Profile
        """
        all_profiles = Profile.objects.all()
        friends = self.get_friends()
        friend_suggestions = [p for p in all_profiles if p not in friends and p != self]
        return friend_suggestions
    

    def get_news_feed(self):
        """
            method to obtain news feed for Profile includes status messages and images
            will return a list (or QuerySet) of all StatusMessages for the profile on which the method was called, as well as all of the friends of that profile
        """
        own_messages = StatusMessage.objects.filter(profile=self)
        friend_messages = StatusMessage.objects.filter(profile__in=self.get_friends())
        all_messages = own_messages.union(friend_messages)
        return list(all_messages)


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


class Friend(models.Model):
    """
        Encapsulate the idea of an edge connecting two nodes within the social network (e.g. two Profiles that are friends with each other).
    """

    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        """
            Return a string representation of this object
        """
        return f'{self.profile1.first_name} {self.profile1.last_name} and {self.profile2.first_name} {self.profile2.last_name} became friends at {self.timestamp}'