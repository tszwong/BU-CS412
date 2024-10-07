# description: the app-specific URLs for the mini_fb application
# mini_fb/urls.py

from django.urls import path
from django.conf import settings
from .views import ShowAllProfilesView
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    # path(r'about', views.about, name="about"), # new page
]