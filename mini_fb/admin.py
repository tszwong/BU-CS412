## Register the models with the Django Admin tool
# mini_fb/admin.py

from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)
