from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.models import User
from agenda.models import Agenda, Consulta, Horario
from agenda.serializers import UserSerializer, AgendaSerializer, ConsultaSerializer, HorarioSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes

import django_filters as filters
import datetime

# ViewSets define the view behavior.
@permission_classes((AllowAny, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        print(request.data)
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return Response({'status': 'Usuario criado'})

@permission_classes((IsAuthenticatedOrReadOnly, ))
class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    

    def create(self, request):
        print(request.data)
        agenda_id = request.data['agenda_id']
        horario_req = request.data['horario']

        agenda = Agenda.objects.get(id=agenda_id)

        horario = Horario.objects.get(agenda=agenda, horario=datetime.datetime.strptime(horario_req, '%H:%M'))

        consulta = Consulta()

        consulta.horario = horario

        username = request.user.get_username()
        user = User.objects.get(username=username)

        consulta.paciente = user

        if Consulta.objects.filter(horario=horario):
            resp = Response({'status': 'Horário já preenchido'})
        else:
            consulta.save()
            resp = Response({'status': 'Consulta criada'})
        
        return resp

    def list(self,request):
        username = None
        if request.user.is_authenticated:
            username = request.user.get_username()
            user = User.objects.get(username=username)
            consultas = Consulta.objects.filter(paciente=user.id)
            return Response(ConsultaSerializer(consultas, many=True).data)

        else:
           return Response({'status': 'Realize o login para acessar as consultas'})


class AgendaViewSet(viewsets.ModelViewSet):
    serializer_class = AgendaSerializer
        
    def get_queryset(self):
        agenda = Agenda.objects.filter(dia_gte=datetime.date.today())
        return agenda

    class AgendaDateFilter(filters.FilterSet):
        dia = filters.DateTimeFromToRangeFilter()

        class Meta:
            model = Agenda
            fields = [
                'medico',
                'medico_especialidade',
                'dia'
            ]

    filter_backends = [DjangoFilterBackend]
    filterset_class = AgendaDateFilter


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

    def list(self,request):
        horarios = Horario.objects.filter(consultas__isnull=True)
        return Response({'status': 'Consulta criada'})