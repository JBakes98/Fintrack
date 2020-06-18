import datetime

import pytz
from django.db import models

from fintrack_be.helpers.timezone_helper import get_timezone, convert_time_to_timezone
from country.models.country import Country


class Exchange(models.Model):
    symbol = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=250, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=False, null=False, default='BST')
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchanges'

    def __str__(self):
        return self.symbol

    def get_stock_count(self):
        """
        Method that returns the number of Stocks on this Exchange
        :return: Number of Stocks
        """
        return self.listed_exchange.count()

    def get_listed_stocks(self):
        """
        Method that returns all of the Stocks on this Exchange
        """
        return self.listed_exchange.all()

    def market_local_time(self):
        """
        Method that gets the markets local time
        """
        timezone = get_timezone(self.timezone, self.country.alpha2)
        pytz_timezone = pytz.timezone(timezone)
        return datetime.datetime.now(pytz_timezone)

    def market_open(self):
        """
        Method that checks if the market is open
        """
        timezone = get_timezone(self.timezone, self.country.alpha2)
        pytz_timezone = pytz.timezone(timezone)
        exchange_time = datetime.datetime.now(pytz_timezone)

        if exchange_time.isoweekday() in range(1, 6):
            if self.opening_time <= exchange_time.time() <= self.closing_time:
                return True
        return False

    def get_market_close_utc(self):
        """
        Method that get the close time of market in UTC
        :return: UTC time of market close
        """
        timezone = get_timezone(self.timezone, self.country.alpha2)
        utc_close = convert_time_to_timezone(self.closing_time, timezone, "UTC")
        return utc_close