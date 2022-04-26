from . import views
from django.urls import path, include

app_name = 'portfolio'

urlpatterns = [
    path('', views.index, name="index"),
    path('update/', views.update, name="update"),
    path('search/', views.search, name="search"),
    path('wallet/', views.wallet, name="wallet"),
    path('buy/', views.buy, name="buy"),
    path('sell/<int:id>', views.sell, name="sell"),
    path('add/', views.add, name="add"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('<str:id>/', views.detail, name="detail"),
]