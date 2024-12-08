from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, HomeView, PortfolioView, SignupView, StockDetailView, WatchlistView, TransactionsView, ProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('stock/<int:pk>/graphs/', StockDetailView.as_view(), name='stock_detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='wt_scrooge_capital/logged_out.html'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]