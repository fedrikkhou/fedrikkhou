from requests_html import HTMLSession
from datetime import datetime
import locale
from decimal import *


class IDNFinancialsStockScraper:
    def __init__(self, session:HTMLSession):
        self.session = session
        self.pageUrl = "https://www.idnfinancials.com/id/"

    def scrapeStock(self, scrapestockcode:str):
        # print(scrapeUrl + scrapeStockCode)
        response = self.session.get(self.pageUrl + scrapestockcode)
        response.html.render(sleep=4)

        prefaceinfo = response.html.xpath("//div[@class='cd-preface-info']//div//text()")
        # ['IDR 370', ' ', '-4 (-1,08%)', 'PT. Midi Utama Indonesia Tbk [MIDI]', 'Sektor:', ' ', 'Layanan Perdagangan dan Investasi', ', ', 'Industri:', ' ', 'Perdagangan Eceran']
        lastPrice = prefaceinfo[0].replace('IDR ', '').replace('.', '')
        companyName = prefaceinfo[3].replace(' [', '').replace(']', '').replace(scrapestockcode, '')
        companySector = prefaceinfo[6]
        companyIndustry = prefaceinfo[10]

        ipoDataHtmlTable = response.html.xpath("//*[@id='table-ipo-dates']//tr//td//text()")
        # ["IPO Date", "31 Mei 2000", "Saham Penawaran", "662.400.000", "Saham Pendiri", "2.252.146.140", "Total Saham Terdaftar", "2.914.546.140", "Persentase", "22,50%", "Harga Penawaran", "1.400 ", "(IDR)", "Dana Terkumpul", "927.360.000.000 ", "(IDR)", "Biro Administrasi Efek", "PT. Raya Saham Registra", "Penjamin Emisi Utama", "PT. Danareksa Sekuritas,\n PT. Bahana Securities", "Papan Pencatatan", "Main"]
        locale.setlocale(locale.LC_ALL, "IND")
        ipoDate = datetime.strptime(ipoDataHtmlTable[1], '%d %B %Y')
        strIpoDate = ipoDate.strftime('%m/%d/%Y')

        ipoNewSharesIssued = Decimal(ipoDataHtmlTable[3].replace('.', ''))
        ownerSharesAmount = Decimal(ipoDataHtmlTable[5].replace('.', ''))
        totalSharesAmount = Decimal(ipoDataHtmlTable[7].replace('.', ''))
        ipoNewSharesIssuedPercentage = Decimal(ipoDataHtmlTable[9].replace('%', '').replace(',', '.'))
        ipoPrice = Decimal(ipoDataHtmlTable[11].replace('.', ''))
        ipoRaisedFund = Decimal(ipoDataHtmlTable[14].replace('.', ''))

        strUnderwriters = ipoDataHtmlTable[19]
        underwriters = strUnderwriters.split(',')
        underwriter1 = underwriters[0].strip()
        underwriter2 = "" if len(underwriters) < 2 else underwriters[1].strip()
        underwriter3 = "" if len(underwriters) < 3 else underwriters[2].strip()

        #for case underwriter empty
        board = ipoDataHtmlTable[len(ipoDataHtmlTable) - 1]

        return [scrapestockcode, companyName, companySector, companyIndustry, lastPrice,
                strIpoDate, ipoPrice, ipoNewSharesIssued, ownerSharesAmount, totalSharesAmount,
                ipoNewSharesIssuedPercentage, ipoRaisedFund, underwriter1, underwriter2, underwriter3,
                board, strUnderwriters]


