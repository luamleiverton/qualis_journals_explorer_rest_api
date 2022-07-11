from rest_framework import viewsets, filters
from qualis.serializers import JournalSerializer
from qualis.models import Journals
from django_filters.rest_framework import DjangoFilterBackend


class JournalViewSet(viewsets.ModelViewSet):
    '''Exibi os journals cadastrados'''
    queryset = Journals.objects.all()
    serializer_class = JournalSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['journal']
    search_fields = ['issn','journal']
    http_method_names=['get']

