from decimal import Decimal

from django.db import models
from django.urls import reverse

from stock.models import Stock
from stock.managers import StockPriceManager
from stock.helpers import timezone_helper as tz_help
from stock.enums import PREDICTION_OPTIONS


class StockPriceData(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    stock = models.ForeignKey(Stock, related_name='stock_prices', on_delete=models.CASCADE)

    high = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    low = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    open = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    close = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    volume = models.BigIntegerField(blank=True, null=True)

    change = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    change_perc = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))

    ml_prediction = models.CharField(max_length=4, choices=PREDICTION_OPTIONS, default=2)

    objects = StockPriceManager()

    class Meta:
        verbose_name = 'Stock Price Data'
        verbose_name_plural = 'Stocks Price Data'
        ordering = ['stock', '-timestamp']

        indexes = [
            models.Index(fields=['timestamp', 'stock']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['stock', 'timestamp'], name='unique_stock_data')
        ]

    def __str__(self):
        string = self.stock.symbol + ' ' + str(self.timestamp)
        return string

    def get_absolute_url(self):
        return reverse('fintrack_be:price', kwargs={'pk': self.pk})

    @property
    def timestamp_in_market_time(self):
        """
        Method that returns the price data timestamp in the market local time from the
        stored UTC time
        :return: Timestamp in local timezone
        """
        timezone = tz_help.get_timezone(self.stock.exchange.timezone, self.stock.exchange.country.alpha2)
        local_timestamp = tz_help.convert_datetime_to_timezone(self.timestamp, "UTC", timezone)
        return local_timestamp
