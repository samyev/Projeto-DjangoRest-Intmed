from medicos.serializer import EspecialidadeSerializer, MedicoSerializer
from medicos.models import Especialidade, Medico
from django.db.models import query
from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class EspecilidadeView(viewsets.ModelViewSet):
  query = Especialidade.objects.all()
  serializer_class = EspecialidadeSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['nome']


class MedicoView(viewsets.ModelViewSet):
  query = Medico.objects.all()
  serializer_class = MedicoSerializer
  filter_backends = [filters.SearchFilter, DjangoFilterBackend]
  search_fields = ['nome']
  filterset_fields = ['especiliadede']