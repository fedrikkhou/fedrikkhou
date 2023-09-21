import csv
import time
from requests_html import HTMLSession
from Scraper.IDNFinancialsStockScraper import IDNFinancialsStockScraper
from Scraper.LembarSahamStockScraper import LembarSahamStockScraper
from Scraper.SahamIdxStockScraper import SahamIdxStockScraper

def scrapeIDNFinancials():
    with open('StockList.csv', newline='') as stockListCsv:
        reader = csv.reader(stockListCsv, delimiter=';', quotechar='"')

        saveintocsv = 'E:\\IDNFinancialsIPOList.csv' #StockIPOList
        with open(saveintocsv, 'a', newline='') as stockIPOListCsv:
            next(reader)

            writer = csv.writer(stockIPOListCsv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writeHeader = True
            #testCode = ['BUKA', 'BBCA', 'GOTO', 'ADRO']
            startFromRow = 1
            endFromRow = 890
            if writeHeader:
                writer.writerow(['No', 'Stock Code', 'Company Name', 'Sector', 'Industry', 'Last Price',
                                 'IPO Date', 'IPO Price', 'IPO New Shares Issued', 'Owner Shares Amount',
                                 'Total Shares Amount',  'IPO New Shares Issued Percentage', 'IPO Raised Fund',
                                 'Underwriter 1', 'Underwriter 2', 'Underwriter 3', 'Board', 'Underwriters' ])

            # Create an HTML session
            session = HTMLSession()
            scrapper = IDNFinancialsStockScraper(session)

            for row in reader:
                rowNumber = row[0]
                if int(rowNumber) >= startFromRow and int(rowNumber) <= endFromRow:
                    print("Reading row: " + rowNumber)
                    stockCode = row[1]
                    scraperesult = scrapper.scrapeStock(stockCode)
                    scraperesult.insert(0, rowNumber)

                    writer.writerow(scraperesult)

            session.close()

def scrapeLembarSaham():
    with open('StockList.csv', newline='') as stockListCsv:
        reader = csv.reader(stockListCsv, delimiter=';', quotechar='"')

        with open('E:\\LembarSahamLastPrice.csv', 'a', newline='') as stockCsv:
            next(reader)

            writer = csv.writer(stockCsv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writeHeader = True
            startFromRow = 1
            endFromRow = 890
            if writeHeader:
                writer.writerow(['No', 'Stock Code', 'Company Name',
                                 'IPO Date', 'Total Number of Shares', 'Market Cap', 'Stock Price'])

            # Create an HTML session
            #pageUrl = "https://lembarsaham.com/fundamental-saham/emiten/"
            scrapper = LembarSahamStockScraper()

            for row in reader:
                rowNumber = row[0]
                if int(rowNumber) >= startFromRow and int(rowNumber) <= endFromRow:
                    print("Reading row: " + rowNumber)
                    stockCode = row[1]
                    scraperesult = scrapper.scrapeStock(stockCode)
                    scraperesult.insert(0, rowNumber)

                    writer.writerow(scraperesult)
                    time.sleep(1)

            print('FINISH SUCCESSFULLY !!')

def scrapeSahamIdx():
    with open('StockList.csv', newline='') as stockListCsv:
        reader = csv.reader(stockListCsv, delimiter=';', quotechar='"')

        saveintocsv = 'E:\\SahamIdxIPOList.csv' #StockIPOList2
        with open(saveintocsv, 'a', newline='') as stockIPOListCsv:
            next(reader)

            writer = csv.writer(stockIPOListCsv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writeHeader = True
            startFromRow = 1
            endFromRow = 890
            if writeHeader:
                writer.writerow(['No', 'Stock Code', 'Company Name',
                                 'Sector', 'Sub Sector', 'Sector ID', 'Sub Sector ID', 'Industry', 'Sub Industry',
                                 'Industry ID', 'Sub Industry ID',
                                 'IPO Date', 'IPO Price', 'IPO Number of Shares', 'Total Number of Shares',
                                 'IPO Shares Percentage', 'Board', 'Underwriters'])

            # Create an HTML session
            scrapper = SahamIdxStockScraper()

            # stockcodetest = ['', 'GGRM', 'BBCA', 'GOTO', 'MBMA', 'PGEO', 'SMSM']
            for row in reader:
                rowNumber = row[0]
                if int(rowNumber) >= startFromRow and int(rowNumber) <= endFromRow:
                    print("Reading row: " + rowNumber)
                    stockCode = row[1]
                    # stockCode = stockcodetest[int(rowNumber)]
                    scraperesult = scrapper.scrapestock(stockCode)
                    scraperesult.insert(0, rowNumber)

                    writer.writerow(scraperesult)
                    time.sleep(1)

            print('FINISH SUCCESSFULLY !!')

#scrapeIDNFinancials()
#scrapeLembarSaham()
scrapeSahamIdx()