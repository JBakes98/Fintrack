from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.industry import *

router = DefaultRouter()
router.register(r'', IndustryViewSet, basename='industry')

urlpatterns = [
    path('companies/', IndustryCompanyListView.as_view(), name='industries_companies'),
    path('<str:name>/companies/', IndustryCompanyRetrieveView.as_view(), name='industry_companies'),
    # path('<str:name>/stocks/', IndustryStockListVIew.as_view()),
]

urlpatterns += router.urls