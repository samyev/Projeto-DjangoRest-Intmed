from django.db.models.base import Model
from rest_framework import serializers
from django.contrib.auth.models import User
from agenda.models import *
from medicos.serializer import MedicoSerializer

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    Model = User
    fields = [
      'url',
      'username',
      'email',
      'password',
    ]


class HorarioSerializer(serializers.ModelSerializer):
  def to_representation(self, value):
    horarios = Horario.objects.filter(consultas__isnull=True)
    if value in horarios:
      return value.get_horario()

  class Meta:
    model = Horario
    fields = ['horario']


class AgendaSerializer(serializers.ModelSerializer):
  medico = MedicoSerializer()
  horarios = serializers.SerializerMethodField('get_horarios')

  def get_horarios(self, requisition):
    print(requisition)
    qs = Horario.objects.filter(consultas_isnull=True, agenda=requisition)
    serializer = HorarioSerializer(instance=qs, many=True)
    return serializer.data
  
  class Meta:
    model = Agenda
    fields = [
      'id',
      'medico',
      'dia',
      'horarios',
    ]


class ConsultaSerializer(serializers.ModelSerializer):
  medico = MedicoSerializer()
  horario = serializers.CharField(source='horario.get_horario')
  dia = serializers.CharField(source='horario.agenda.get_dia')

  class Meta:
    model = Consulta
    fields = [
      'id',
      'dia',
      'horario',
      'data_agendamento',
      'medico',
    ]