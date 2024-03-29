from exchange.services import ExchangeClass
from stock.services import StockDataService
import requests
import bs4 as bs
import datetime


class NYSE(ExchangeClass):
    """
    ExchangeClass child
    """
    def __init__(self):
        self._name = 'New York Stock Exchange'
        self._symbol = 'NYSE'
        self._stock_links = ('http://eoddata.com/stocklist/NYSE/A.htm/',
                            'http://eoddata.com/stocklist/NYSE/B.htm/',
                            'http://eoddata.com/stocklist/NYSE/C.htm/',
                            'http://eoddata.com/stocklist/NYSE/D.htm',
                            'http://eoddata.com/stocklist/NYSE/E.htm',
                            'http://eoddata.com/stocklist/NYSE/F.htm',
                            'http://eoddata.com/stocklist/NYSE/G.htm',
                            'http://eoddata.com/stocklist/NYSE/H.htm',
                            'http://eoddata.com/stocklist/NYSE/I.htm',
                            'http://eoddata.com/stocklist/NYSE/J.htm',
                            'http://eoddata.com/stocklist/NYSE/K.htm',
                            'http://eoddata.com/stocklist/NYSE/L.htm',
                            'http://eoddata.com/stocklist/NYSE/M.htm',
                            'http://eoddata.com/stocklist/NYSE/N.htm',
                            'http://eoddata.com/stocklist/NYSE/O.htm',
                            'http://eoddata.com/stocklist/NYSE/P.htm',
                            'http://eoddata.com/stocklist/NYSE/Q.htm',
                            'http://eoddata.com/stocklist/NYSE/R.htm',
                            'http://eoddata.com/stocklist/NYSE/S.htm',
                            'http://eoddata.com/stocklist/NYSE/T.htm',
                            'http://eoddata.com/stocklist/NYSE/U.htm',
                            'http://eoddata.com/stocklist/NYSE/V.htm',
                            'http://eoddata.com/stocklist/NYSE/W.htm',
                            'http://eoddata.com/stocklist/NYSE/X.htm',
                            'http://eoddata.com/stocklist/NYSE/Y.htm',
                            'http://eoddata.com/stocklist/NYSE/Z.htm',)
        self._country = 'US'
        self._timezone = 'EST'
        self._opening_time = datetime.time(hour=9, minute=30)
        self._closing_time = datetime.time(hour=16)

    def create_stocks(self):
        """ Function for creating classes stocks """
        for link in self.stock_links:
            resp = requests.get(link)
            soup = bs.BeautifulSoup(resp.text, "lxml")
            table = soup.find('table', {'class': 'quotes'})

            for row in table.findAll('tr')[1:]:
                ticker = row.findAll('td')[0].text
                mapping = str.maketrans(".", "-")
                ticker = ticker.translate(mapping)
                name = row.findAll('td')[1].text
                StockDataService(ticker=ticker, name=name, exchange=self._symbol).create_stock()
