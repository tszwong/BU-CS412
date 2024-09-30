# description: the app-specific URLs for the formdata application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path("", views.main, name="main"),
    path(r'order', views.order, name="order"),
    # path(r'restaurant', views.restaurant_redirect, name="restaurant_redirect"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]