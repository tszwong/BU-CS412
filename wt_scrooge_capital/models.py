from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.company_name} ({self.ticker})"
    

class StockPriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="price_history")
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=50)
    type = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.stock.ticker} on {self.date}"


class Portfolio(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="portfolio")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()


    def __str__(self):
        return f"{self.user}'s portfolio - {self.stock.ticker}"


class WatchList(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="watchlist")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    added_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_date = models.DateField(auto_now_add=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"{self.user}'s watchlist - {self.stock.ticker}"


class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="transactions")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_CHOICES)

    class Meta:
        ordering = ['-purchase_date'] 

    def __str__(self):
        return f"{self.user} {self.transaction_type} {self.stock.ticker}"
