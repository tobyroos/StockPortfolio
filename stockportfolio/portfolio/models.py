from django.db import models
import datetime

# Create your models here.


class WalletModel(models.Model):

    def __str__(self):
        return str(self.money_field)

    money_field = models.DecimalField(max_digits=50, decimal_places=2, default=0)


class StockModel(models.Model):
    def __str__(self):
        return self.symbol_field

    def net_gain(self):
        return round(self.price_field * self.shares_field, 2) - round(self.price_bought_field, 2)

    def market_value(self):
        return round(self.price_field * self.shares_field, 2)

    symbol_field = models.CharField(max_length=5)
    name_field = models.CharField(max_length=200)
    sector_field = models.CharField(max_length=200)
    currency_field = models.CharField(max_length=25)
    price_field = models.DecimalField(max_digits=50, decimal_places=2)
    price_bought_field = models.DecimalField(max_digits=50, decimal_places=2)
    date_bought_field = models.DateField(default=datetime.date.today)
    shares_field = models.DecimalField(max_digits=50, decimal_places=2)

class BuyModel(models.Model):
    def __str__(self):
        return self.symbol_field

    symbol_field = models.CharField(max_length=5)
    name_field = models.CharField(max_length=200)
    sector_field = models.CharField(max_length=200)
    currency_field = models.CharField(max_length=25)
    price_field = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    date_bought_field = models.DateField(default=datetime.date.today)

