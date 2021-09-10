from rest_framework import serializers
from django.contrib.auth.models import User
from medicos.models import Especialidade, Medico


class EspecialidadeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id','nome']


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer()
    class Meta:
        model = Medico
        fields = ['id','crm', 'nome', 'especialidade']