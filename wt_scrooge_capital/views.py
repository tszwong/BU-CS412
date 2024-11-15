from django.shortcuts import render, redirect
from .models import Transaction, UserProfile, Portfolio, WatchList, Stock
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin 


class HomeView(LoginRequiredMixin, ListView):
    """
        Create a subclass of ListView
    """

    model = Stock
    template_name = 'wt_scrooge_capital/home.html'
    context_object_name = 'stocks'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile
        context['stocks'] = Stock.objects.all()
        return context
     

class PortfolioView(LoginRequiredMixin, ListView):
    """
        Create a subclass of ListView
    """

    model = Portfolio
    template_name = 'wt_scrooge_capital/portfolio.html'
    context_object_name = 'portfolio'


    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile
        return context
    

class WatchlistView(LoginRequiredMixin, ListView):
    """
        Create a subclass of ListView
    """

    model = WatchList
    template_name = 'wt_scrooge_capital/watchlist.html'
    context_object_name = 'watchlist'


    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile
        return context
    

class TransactionsView(LoginRequiredMixin, ListView):
    """
        Create a subclass of ListView
    """

    model = Transaction
    template_name = 'wt_scrooge_capital/transactions.html'
    context_object_name = 'transactions'


    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile
        return context
    

class ProfileView(LoginRequiredMixin, ListView):
    """
        Create a subclass of ListView
    """

    model = UserProfile
    template_name = 'wt_scrooge_capital/profile.html'
    context_object_name = 'profile'


    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile
        context['stocks'] = Stock.objects.all()
        context['transactions'] = Transaction.objects.all()
        return context