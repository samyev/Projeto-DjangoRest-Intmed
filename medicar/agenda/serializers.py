from datetime import datetime

from rest_framework import serializers
from django.contrib.auth.models import User
from agenda.models import Agenda, Consulta, Horario
from medicos.serializers import MedicoSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            'url', 'username', 'is_staff'
            'email', 'password'
        ]
        read_only_fields = ['is_staff']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return user


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

    def get_horarios(self, product):
        qs = Horario.objects.filter(consultas__isnull=True,agenda=product)
        serializer = HorarioSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Agenda
        fields = ['id', 'medico', 'dia', 'horarios']


class ConsultaWriteSerializer(serializers.ModelSerializer):
    agenda_id = serializers.PrimaryKeyRelatedField(
        queryset=Agenda.objects.all(), write_only=True
    )
    horario = serializers.TimeField(
        input_formats=["%H:%M"], write_only=True
    )

    class Meta:
        model = Consulta
        fields = (
            'agenda_id', 'horario'
        )

    def validate(self, data):
        request = self.context['request']

        user = request.user
        agenda = data['agenda_id']
        horario = data['horario']

        dia = agenda.dia

        data_consulta = datetime(
            dia.year, dia.month, dia.day, horario.hour, horario.minute
        )

        if data_consulta < datetime.now():
            raise serializers.ValidationError("Dia já passou")

        consultas = Consulta.objects.filter(paciente=user)

        consultas = consultas.filter(
            horario__horario=horario,
            horario__agenda__dia=dia
        )

        if consultas.exists():
            raise serializers.ValidationError(
                "Você já tem consulta marcada neste horário"
            )

        consultas = Consulta.objects.all()

        consultas = consultas.filter(
            horario__horario=horario,
            horario__agenda__dia=dia
        )

        if consultas.exists():
            raise serializers.ValidationError(
                "Já existe consulta marcada nesse horário"
            )

        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        agenda = validated_data['agenda_id']
        horario = validated_data['horario']

        horario = Horario.objects.filter(
            agenda=agenda, horario=horario
        ).first()

        consulta = Consulta.objects.create(
            paciente=user, horario=horario
        )

        return consulta


class ConsultaReadSerializer(serializers.ModelSerializer):
    dia = serializers.DateField(
        source="horario.agenda.dia", read_only=True
    )
    horario = serializers.TimeField(
        source="horario.horario", read_only=True
    )
    medico = MedicoSerializer(read_only=True)

    class Meta:
        model = Consulta
        fields = [
            'id', 'dia', 'horario', 'data_agendamento',
            'medico'
        ]
        read_only_fields = ['data_agendamento']