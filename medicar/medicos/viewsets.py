from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from medicos.models import Especialidade, Medico

from medicos.serializers import EspecialidadeSerializer, MedicoSerializer 


# ViewSets define the view behavior.
class EspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nome']
    filterset_fields = ['especialidade']