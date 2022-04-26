from django.shortcuts import render, redirect
from .models import StockModel
from .models import WalletModel
from .models import BuyModel
import yfinance as yf
import plotly.express as px
from decimal import *

# Create your views here.


def index(request):
    data = StockModel.objects.all()

    for stockName in data:
        stock = yf.Ticker(stockName.symbol_field)

        currentPrice = str(stock.info['currentPrice'])
        stockName.price = Decimal(currentPrice)

        stockName.save()

    return render(request, 'portfolio/index.html', {'data': data})


def search(request):

    if request.method == 'POST':
        sym = request.POST.get('sym', '').upper()
        stock = yf.Ticker(sym)
        BuyModel.objects.all().delete()
        try:
            currentPrice = str(stock.info['currentPrice'])
            currentPrice = Decimal(currentPrice)
            BuyModel.objects.create(symbol=sym, price=currentPrice)
        except:
            print("Not Valid")
    else:
        BuyModel.objects.all().delete()
    data = BuyModel.objects.all()
    return render(request, 'portfolio/search.html', {'data': data})


def buy(request):
    data = BuyModel.objects.all()
    walletData = WalletModel.objects.all()
    if request.method == 'POST':
        shares = str(request.POST.get('share', ''))
        shares = Decimal(shares)
        symbol = ""
        wallet = Decimal(0)
        price = Decimal(0)
        for stock in data:
            symbol = stock.symbol
            price = Decimal(stock.price * shares)
        for w in walletData:
            wallet = Decimal(w.money_field)

        if wallet >= price:
            try:
                StockModel.objects.create(symbol_field=symbol, price_bought_field=price, shares_field=shares)
                for w in walletData:
                    w.money_field -= price
                    w.save()
                print("You bought ", symbol)
            except:
                print("Failed to buy stock")

            data = StockModel.objects.all()
            return redirect('portfolio:index')
        else:
            print("Could not afford stock")
            data = BuyModel.objects.all()
            return redirect('portfolio:search')
    else:
        data = BuyModel.objects.all()
        return redirect('portfolio:search')


def wallet(request):
    money = WalletModel.objects.all()
    return render(request, 'portfolio/wallet.html', {'data': money})


def add(request):
    data = WalletModel.objects.all()

    if request.method == 'POST':
        fund = str(request.POST.get('add', ''))
        fund = Decimal(fund)

        for wallet in data:
            money = Decimal(wallet.money_field)
            wallet.money_field = fund + money
            wallet.save()

    else:
        print("Failed to add funds")
    return redirect('portfolio:wallet')


def withdraw(request):
    data = WalletModel.objects.all()

    if request.method == 'POST':
        fund = str(request.POST.get('withdraw', ''))
        fund = Decimal(fund)

        for wallet in data:
            money = Decimal(wallet.money_field)
            wallet.money_field = money - fund
            if wallet.money_field >= Decimal(0):
                wallet.save()
            else:
                print("Failed to withdraw funds")
    else:
        print("Failed to withdraw funds")
    return redirect('portfolio:wallet')


def detail(request, id):
    if request.method == 'POST':
        period = request.POST.get('filter', '')
    else:
        period = '7d'

    stock_model = StockModel.objects.get(symbol_field=id)
    stock = yf.Ticker(id)
    stock_info = stock.info
    stockPlot = stock.history(period)

    stockPlot = stockPlot.drop(columns=['Open','High','Low','Dividends','Stock Splits', 'Volume'])

    fig = px.line(
        x=[row[0] for row in stockPlot.itertuples()],
        y=[round(row[1], 2) for row in stockPlot.itertuples()],
        title = id + " " + period + " History",
        labels = {'x': 'Date', 'y': 'Price'}
    )

    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })

    chart = fig.to_html()

    context = {'stock_model': stock_model, 'stock': stock_info, 'chart': chart}

    return render(request, 'portfolio/detail.html', context)


def sell(request, id):
    print("Sell")
    stock = StockModel.objects.get(id=id)
    wallet = WalletModel.objects.all()
    value = getattr(stock, "price")
    share = getattr(stock, "shares_field")
    value = Decimal(value * share)

    if request.method == 'POST':
        print("POST")
        for w in wallet:
            money = Decimal(w.money_field)
            w.money_field = value + money
            w.save()
        stock.delete()
        return redirect('portfolio:index')

    return redirect('portfolio:detail', stock.symbol_field)
