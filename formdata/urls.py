# description: the app-specific URLs for the formdata application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]