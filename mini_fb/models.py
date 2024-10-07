# mini_fb/models.py

from django.db import models

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
    
    def __str__(self):
        """
            Return a string representation of this Profile object.
        """
        return f'{self.first_name} {self.last_name} from {self.city}'
