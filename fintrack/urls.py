from django.contrib import admin
from django.urls import path, include
from fintrack import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('fintrack_be.urls.base_urls')),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/country/', include('country.urls')),
    path('api/v1/sector/', include('sector.urls')),
    path('', views.index),
]
