# description: the app-specific URLs for the mini_fb application
# mini_fb/urls.py

from django.urls import path
from django.conf import settings
from .views import CreateProfileView, CreateStatusMessageView, ShowAllProfilesView, ShowProfilePageView, ProfileListView
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    # path(r'about', views.about, name="about"), # new page
]