from . import views
from django.urls import path, include

app_name = 'portfolio'

urlpatterns = [
    path('', views.start, name="start"),
    path('portfolio/', views.index, name="index"),
    path('portfolio/update/', views.update, name="update"),
    path('portfolio/search/', views.search, name="search"),
    path('portfolio/wallet/', views.wallet, name="wallet"),
    path('portfolio/buy/', views.buy, name="buy"),
    path('portfolio/sell/<int:id>', views.sell, name="sell"),
    path('portfolio/add/', views.add, name="add"),
    path('portfolio/withdraw/', views.withdraw, name="withdraw"),
    path('portfolio/<str:id>/', views.detail, name="detail"),
]