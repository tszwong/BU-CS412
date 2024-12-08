from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Transaction, UserProfile, Portfolio, WatchList, Stock, StockPriceHistory
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm, SignupForm
from django.views.generic.edit import FormView
import plotly.express as px
from plotly.io import to_html


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'wt_scrooge_capital/login.html'


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
        Displays the user's portfolio.
    """
    model = Portfolio
    template_name = 'wt_scrooge_capital/portfolio.html'
    context_object_name = 'portfolio'

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Portfolio.objects.filter(user=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        portfolio_items = Portfolio.objects.filter(user=user_profile)

        for item in portfolio_items:
            item.total_value = item.shares * item.stock.current_price
        
        context['portfolio'] = portfolio_items
        context['portfolio_total_shares'] = sum(item.shares for item in portfolio_items)
        context['portfolio_total_value'] = sum(item.shares * item.stock.current_price for item in portfolio_items)

        return context

    

class WatchlistView(LoginRequiredMixin, ListView):
    """
        Create a subclass of ListView
    """

    model = WatchList
    template_name = 'wt_scrooge_capital/watchlist_expanded.html'
    context_object_name = 'watchlist'


    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return WatchList.objects.filter(user=user_profile)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile
        return context
    

class TransactionsView(LoginRequiredMixin, ListView):
    """
        Displays the transaction history for the logged-in user.
    """
    model = Transaction
    template_name = 'wt_scrooge_capital/transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        # Filter transactions for the logged-in user's profile
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Transaction.objects.filter(user=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = user_profile  # Optional: Pass the profile for additional context
        return context
    

class ProfileView(LoginRequiredMixin, ListView):
    """
        Displays the profile page for the logged-in user.
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
        context['transactions'] = Transaction.objects.filter(user=user_profile)
        return context


class SignupView(FormView):
    """
        View for user registration
    """
    template_name = 'wt_scrooge_capital/signup.html'
    form_class = SignupForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    

class StockDetailView(LoginRequiredMixin, DetailView):
    """
        Detailed view of a single Stock record, including price history and graphs.
    """
    model = Stock
    template_name = 'wt_scrooge_capital/stock_detail.html'
    context_object_name = 'stock'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object
        price_history_record = StockPriceHistory.objects.filter(stock=stock).first()

        if price_history_record and price_history_record.price_history:
            price_history = [
                float(price.strip()) for price in price_history_record.price_history.strip("[]").split(",")
            ]
            hours = [f"{hour}:00" for hour in range(1, len(price_history) + 1)]
            line_color = 'rgb(0, 200, 5)' if price_history[-1] > price_history[0] else 'rgb(255, 80, 0)'

            price_chart = px.line(
                x=hours,
                y=price_history,
                labels={"x": "Hour", "y": "Price ($)"},
                title=f"{stock.company_name} ({stock.ticker}) - 12-Hour Price History",
            )
            price_chart.update_traces(
                mode="lines+markers",
                line=dict(color=line_color),
            )
            price_chart.update_layout(
                width=900,
                height=600,
                # plot_bgcolor="rgba(30, 30, 30, 1)",
                title_font=dict(size=18),
                xaxis_title_font=dict(size=14),
                yaxis_title_font=dict(size=14),
            )

            context['open_price'] = price_history_record.open_price
            context['close_price'] = price_history_record.close_price
            context['region'] = price_history_record.region
            context['type'] = price_history_record.type
            context['price_chart'] = to_html(price_chart, full_html=False)
            context['max_price'] = max(price_history)
            context['min_price'] = min(price_history)
            context['diff'] = context['close_price'] - context['open_price']


        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            portfolio_item = Portfolio.objects.filter(user=user_profile, stock=stock).first()
            context['shares_owned'] = portfolio_item.shares if portfolio_item else 0
        else:
            context['shares_owned'] = 0


        return context
