from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Country
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers.country import CountryExchangeSerializer


class CountryExchangeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CountryExchangeSerializer
    queryset = Country.objects.all()


class CountryExchangeRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = CountryExchangeSerializer

    def get_object(self):
        alpha2 = self.kwargs['alpha2']
        return get_object_or_404(Country, alpha2=alpha2)
