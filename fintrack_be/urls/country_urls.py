from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views import *

router = DefaultRouter()
router.register(r'', CountryViewSet, basename='country')

urlpatterns = [
    path('exchanges/', CountryExchangeListView.as_view(), name='countries_exchanges'),
    path('<str:alpha2>/exchanges/', CountryExchangeRetrieveView.as_view(), name='country_exchanges'),
]

urlpatterns += router.urls
