from django.contrib import admin
from .models import StockModel
from .models import WalletModel
from .models import BuyModel

# Register your models here.


admin.site.register(StockModel)
admin.site.register(WalletModel)
admin.site.register(BuyModel)
