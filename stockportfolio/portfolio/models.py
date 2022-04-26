from django.db import models
import datetime

# Create your models here.


class WalletModel(models.Model):

    def __str__(self):
        return self.money_field

    money_field = models.DecimalField(max_digits=50, decimal_places=2, default=0)


class StockModel(models.Model):
    def __str__(self):
        return self.symbol_field

    def net_gain(self):
        return round(self.price * self.shares_field, 2) - round(self.price_bought_field, 2)

    def market_value(self):
        return round(self.price * self.shares_field, 2)

    symbol_field = models.CharField(max_length=5)
    date_bought_field = models.DateField(default=datetime.date.today)
    price_bought_field = models.DecimalField(max_digits=50, decimal_places=2)
    shares_field = models.DecimalField(max_digits=50, decimal_places=2)
    price = models.DecimalField(max_digits=50, decimal_places=2, default=0)

class BuyModel(models.Model):
    def __str__(self):
        return self.symbol

    symbol = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=50, decimal_places=2)

