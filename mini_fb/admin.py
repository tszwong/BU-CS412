## Register the models with the Django Admin tool
# mini_fb/admin.py

from django.contrib import admin
from .models import Friend, Image, Profile, StatusMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)