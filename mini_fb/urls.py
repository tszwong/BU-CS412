# description: the app-specific URLs for the mini_fb application
# mini_fb/urls.py

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import CreateFriendView, CreateProfileView, CreateStatusMessageView, DeleteStatusMessageView, ShowAllProfilesView, \
    ShowProfilePageView, ProfileListView, UpdateProfileView, UpdateStatusMessageView, ShowFriendSuggestionsView, ShowNewsFeedView
from . import views

# create a list of URLs for this app
urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    # path('profile/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('status/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="add_friend"),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]