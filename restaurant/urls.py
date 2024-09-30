# description: the app-specific URLs for the formdata application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path("main/", views.main, name="main"),
    path("order/", views.order, name="order"),
    path("confirmation/", views.confirmation, name="confirmation"),
]