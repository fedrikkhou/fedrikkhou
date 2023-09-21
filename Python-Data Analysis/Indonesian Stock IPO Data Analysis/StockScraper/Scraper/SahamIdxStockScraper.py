import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

class SahamIdxStockScraper:
    def __init__(self):
        self.pageUrl = "https://sahamidx.com/?view=Stock.Profile&path=Stock&stock_code="

    def scrapestock(self, scrapestockcode:str):
        #print(scrapeurl + scrapestockcode)

        try:
            page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
        except requests.exceptions.Timeout:
            print('Requests Get Url Timeout, retrying')
            page = requests.get(self.pageUrl + scrapestockcode, timeout=5)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)

        print('Requests Get Url Success')
        # with open("C:\\Users\\FEDRIK\\PycharmProjects\\pythonProject\\SahamIdxTest.html") as fp:
        #   soup = BeautifulSoup(fp, 'html.parser')
        soup = BeautifulSoup(page.content, 'html.parser')

        #cant use id or class, so use find all n get the no 6 table
        table = soup.find_all('table')[5]
        rows = table.find_all('tr')

        ipoprice = iposharesamount = totalsharesamount = iposharespercentage = underwriters1 = 'ERROR'
        underwriters2 = ''
        sector = subsector = sectorid = subsectorid = '-'
        industry = subindustry = industryid = subindustryid = '-'
        for row in rows:
            if 'Nama Member' in row.text:
                companyname = row.find_all('td')[2].text.strip()
            elif 'Tanggal IPO' in row.text:
                stripodate = row.find_all('td')[2].text.strip()
            elif 'Harga IPO' in row.text:
                ipoprice = row.find_all('td')[2].text.strip()
            elif 'IPO Saham' in row.text:
                iposharesamount = row.find_all('td')[2].text.strip()
            elif 'Total Saham' in row.text:
                totalsharesamount = row.find_all('td')[2].text.strip()
            elif 'Persentase IPO' in row.text:
                iposharespercentage = row.find_all('td')[2].text.strip()
            elif 'Penjamin Pelaksana Emisi Efek' in row.text:
                # underwriters use enter <br> as delimiter, all html tags will be removed
                underwriters1 = str(row.find_all('td')[2].contents[0]).replace('<b>', '').replace('</b>', '').replace('<br/>', '||')
            elif 'Penjamin Emisi Efek' in row.text:
                underwriters2 = str(row.find_all('td')[2].contents[0]).replace('<b>', '').replace('</b>', '').replace('<br/>', '||')
            elif 'Papan' in row.text:
                board = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Sector':
                sector = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Sub Sector':
                subsector = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Sector ID':
                sectorid = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Sub Sector ID':
                subsectorid = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Industry':
                industry = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Sub Industry':
                subindustry = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Industry ID':
                industryid = row.find_all('td')[2].text.strip()
            elif row.find_all('td')[0].text.strip() == 'Sub Industry ID':
                subindustryid = row.find_all('td')[2].text.strip()

        # format: Fri, 24-Feb-2023
        locale.setlocale(locale.LC_ALL, "en")
        ipodate = datetime.strptime(stripodate, '%a, %d-%b-%Y')
        stripodate = ipodate.strftime('%m/%d/%Y')

        ipoprice = ipoprice.replace('Rp. ', '').replace('.', '').replace(',', '').replace('.', '').replace('-', '')
        iposharesamount = iposharesamount.replace(' Lembar', '').replace(',', '').replace('.', '')
        totalsharesamount = totalsharesamount.replace(' Lembar', '').replace(',', '').replace('.', '')
        iposharespercentage = iposharespercentage.replace('%', '').replace(',', '.')

        if underwriters2 != '':
            underwriters = underwriters1 + '||' + underwriters2
        else:
            underwriters = underwriters1

        stockdata = [scrapestockcode, companyname, sector, subsector, sectorid, subsectorid,
                     industry, subindustry, industryid, subindustryid,
                      stripodate, ipoprice, iposharesamount, totalsharesamount, iposharespercentage, board,
                      underwriters]
        #print(stockdata)
        return stockdata






