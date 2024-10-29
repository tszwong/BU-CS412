# description: the app-specific URLs for the mini_fb application
# mini_fb/urls.py

from django.urls import path
from django.conf import settings
from .views import CreateFriendView, CreateProfileView, CreateStatusMessageView, DeleteStatusMessageView, ShowAllProfilesView, \
    ShowProfilePageView, ProfileListView, UpdateProfileView, UpdateStatusMessageView, ShowFriendSuggestionsView, ShowNewsFeedView
from . import views

# create a list of URLs for this app
urlpatterns = [
    # path(url, view, name)
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('update_profile/<int:pk>', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:profile_pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="add_friend"),
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),
    # path(r'about', views.about, name="about"), # new page
]