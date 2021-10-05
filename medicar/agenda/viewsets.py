import datetime

import django_filters as filters

from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from agenda.models import Agenda, Consulta, Horario
from agenda.serializers import (
    UserSerializer, AgendaSerializer, ConsultaReadSerializer,
    ConsultaWriteSerializer, HorarioSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def check_object_permissions(self, request, obj):
        if request.user.is_superuser:
            return

        if not request.user == obj:
            self.permission_denied(
                request,
                message="não pode cara",
                code=status.HTTP_403_FORBIDDEN
            )


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaWriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        consulta = serializer.save()

        serializer = ConsultaReadSerializer(consulta)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        username = None
        if request.user.is_authenticated:
            username = request.user.get_username()
            user = User.objects.get(username=username)
            consultas = Consulta.objects.filter(paciente=user.id)
            return Response(ConsultaReadSerializer(consultas, many=True).data)

        else:
            return Response(
                {
                   'status': 'Realize o login para acessar as consultas'
                }
            )


class AgendaViewSet(viewsets.ModelViewSet):
    serializer_class = AgendaSerializer

    def get_queryset(self):
        agenda = Agenda.objects.filter(dia__gte=datetime.date.today())
        return agenda

    class AgendaDateFilter(filters.FilterSet):
        dia = filters.DateTimeFromToRangeFilter()

        class Meta:
            model = Agenda
            fields = [
                'medico',
                'medico__especialidade',
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