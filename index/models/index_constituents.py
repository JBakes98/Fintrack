from django.db import models
from index.models.index import Index
from stock.models import Stock


class IndexConstituents(models.Model):
    constituent = models.ForeignKey(Stock, on_delete=models.CASCADE)
    index = models.ForeignKey(Index, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Index Constituents'
        verbose_name_plural = 'Indices Constituents'
        ordering = ['index', 'constituent']

        constraints = [
            models.UniqueConstraint(fields=['constituent', 'index'], name='index_constituent')
        ]