from rest_framework import serializers
from medicos.models import Medico, Especialidade

class EspecialidadeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Especialidade
    fields = [
      "id", 
      "nome",
    ]


class MedicoSerializer(serializers.ModelSerializer):
  especialidade = EspecialidadeSerializer()

  class Meta:
    model = Medico
    fields = [
      "id",
      "nome",
      "crm"
      "Especialidade",
    ]