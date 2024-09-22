# description: the app-specific URLs for the quotes application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path(r'', views.home, name="home"), # name should match the function name, main page, first url
    path(r'about', views.about, name="about"), # new page
    path(r'quote', views.quote, name="quote"), # new page
    path(r'show_all', views.show_all, name="show_all"), # new page
]