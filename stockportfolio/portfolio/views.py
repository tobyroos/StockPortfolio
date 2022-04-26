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
    return render(request, 'portfolio/index.html', {'data': data})


def update(request):
    data = StockModel.objects.all()

    for stockName in data:
        stock = yf.Ticker(stockName.symbol_field)

        currentPrice = str(stock.info['currentPrice'])
        stockName.price = Decimal(currentPrice)

        stockName.save()

    return redirect('portfolio:index')


def search(request):

    if request.method == 'POST':
        symbol = request.POST.get('sym', '').upper()
        stock = yf.Ticker(symbol)
        BuyModel.objects.all().delete()
        try:
            name = str(stock.info['longName'])
            sector = str(stock.info['sector'])
            currency = str(stock.info['currency'])
            price = Decimal(str(stock.info['currentPrice']))
            BuyModel.objects.create(symbol_field=symbol, name_field=name, sector_field=sector, currency_field=currency, price_field=price)
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

        symbol = ""
        name = ""
        sector = ""
        currency = ""
        price = Decimal(0)
        price_bought = Decimal(0)
        shares = Decimal(str(request.POST.get('share', '')))

        for stock in data:
            symbol = stock.symbol_field
            name = stock.name_field
            sector = stock.sector_field
            currency = stock.currency_field
            price = Decimal(stock.price_field)
            price_bought = price * shares

        wallet = Decimal(0)
        for w in walletData:
            wallet = Decimal(w.money_field)

        if wallet >= price_bought:
            try:
                StockModel.objects.create(symbol_field=symbol, name_field=name, sector_field=sector,
                                          currency_field=currency, price_field=price,
                                          price_bought_field=price_bought, shares_field=shares)
                for w in walletData:
                    w.money_field -= price_bought
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

    context = {'stock': stock_model, 'chart': chart}

    return render(request, 'portfolio/detail.html', context)


def sell(request, id):
    print("Sell")
    stock = StockModel.objects.get(id=id)
    wallet = WalletModel.objects.all()
    value = getattr(stock, "price_field")
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
