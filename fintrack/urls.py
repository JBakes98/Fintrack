from django.contrib import admin
from django.urls import path, include
from fintrack import views


urlpatterns = [
    path('console/', admin.site.urls),
    path('', include('fintrack_fe.urls')),
    path('v1/user/', include('fintrack_be.urls.user_urls')),
    path('v1/country/', include('fintrack_be.urls.country_urls')),
    path('v1/sector/', include('fintrack_be.urls.sector_urls')),
    path('v1/industry/', include('fintrack_be.urls.industry_urls')),
    path('v1/exchange/', include('fintrack_be.urls.exchange_urls')),
    path('v1/company/', include('fintrack_be.urls.company_urls')),
    path('v1/stock/', include('fintrack_be.urls.stock_urls')),
    path('v1/index/', include('fintrack_be.urls.index_urls')),
    path('v1/email-list/', include('fintrack_be.urls.mail_list_urls')),
    path('v1/position/', include('fintrack_be.urls.position_urls'))
]
