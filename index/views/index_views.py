from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from index.models import Index
from index.serializers import IndexSerializer, IndexCorrelationSerializer
from fintrack.permissions import IsVerified
from index.services.IndexMachineLearningService import IndexMachineLearningService


class IndexListView(generics.ListAPIView):
    """
    Retrieve a list of all Index instances
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndexSerializer

    def get_queryset(self):
        return Index.objects.all().order_by('symbol')


class IndexCorrelationAPIView(generics.ListAPIView):
    """
    Retrieve correlation data of an Indices constituents
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, symbol):
        try:
            return Index.objects.get(symbol=symbol)
        except Index.DoesNotExist:
            raise Http404

    def get(self, request, symbol, format=None):
        index = Index.objects.get(symbol=self.get_object(symbol))
        index_service = IndexMachineLearningService()
        df = index_service.get_index_constituent_correlation(index.pk)
        serializer = IndexCorrelationSerializer(df.to_dict())
        print(serializer.data)
        return Response(df.to_json())