# description: the app-specific URLs for the voter_analytics application
# voter_analytics/urls.py

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from .views import VoterDetailView, VoterGraphsView, VotersView


# create a list of URLs for this app
urlpatterns = [
    path('', VotersView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]