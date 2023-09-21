import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from decimal import *


class LembarSahamStockScraper:

    def __init__(self):
        self.pageUrl = "https://lembarsaham.com/fundamental-saham/emiten/"

    def scrapeStock(self, scrapestockcode:str):
        #print(scrapeurl + scrapestockcode)

        try:
            page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
        except requests.exceptions.Timeout:
            try:
                print('Requests Get Url Timeout, retrying')
                page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
            except requests.exceptions.Timeout:
                try:
                    print('Requests Get Url Timeout, retrying')
                    page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
                except requests.exceptions.Timeout:
                    try:
                        print('Requests Get Url Timeout, retrying')
                        page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
                    except requests.exceptions.Timeout:
                        print('Requests Get Url Timeout, retrying')
                        page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)

        print('Requests Get Url Success')
        soup = BeautifulSoup(page.content, 'html.parser')

        companyName = soup.find('h1', attrs={'class': 'header header-company'}).text.replace('\\n', '').replace(
            scrapestockcode + ' - ', '').strip()

        divStockProfile = soup.find('div', attrs={'class': 'profile-content row'})

        stockData = divStockProfile.findAll('div', attrs={'class': 'col-sm-9'})

        #sector = stockData[2].text.replace('\\r\\n', '').strip()
        #subsector = stockData[3].text.replace('\\r\\n', '').strip()
        #industry = stockData[4].text.replace('\\r\\n', '').strip()
        #subindustry = stockData[5].text.replace('\\r\\n', '').strip()

        locale.setlocale(locale.LC_ALL, "IND")
        ipoDate = datetime.strptime(stockData[7].text.replace('\\r\\n', '').strip(), '%d %B %Y')
        strIpoDate = ipoDate.strftime('%m/%d/%Y')

        board = stockData[8].text.replace('\\r\\n', '').strip()

        # sample: 31.985.962.000 lembar / 31,99 M lembar
        totalofshares = Decimal(
            stockData[9].text.replace('\\r\\n', '').split('/')[0].replace('lembar', '').replace('.', '').strip())
        strmarketcap = stockData[10].text.replace('\\r\\n', '').replace('Rp. ', '').strip()
        marketcap = 0
        if strmarketcap.endswith('T'):
            # 1 triliun = 1.000.000.000.000
            strmarketcap = strmarketcap.replace('Rp.', '').replace('.', '').replace(',', '.').replace(' T', '').strip()
            marketcap = Decimal(strmarketcap) * 1000000000000
        elif strmarketcap.endswith('M'):
            # 1 miliar = 1.000.000.000
            strmarketcap = strmarketcap.replace('Rp.', '').replace('.', '').replace(',', '.').replace(' M', '').strip()
            marketcap = Decimal(strmarketcap) * 1000000000

        stockprice = round(marketcap / totalofshares)

        return [scrapestockcode, companyName,
                strIpoDate, totalofshares, marketcap, stockprice]






