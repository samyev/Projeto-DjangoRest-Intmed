from django.contrib import admin
from agenda.models import Agenda, Consulta, Horario


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('medico', 'dia')
admin.site.register(Agenda, AgendaAdmin)


class HorarioAdmin(admin.ModelAdmin):
    list_display = ('horario', 'data','medico','paciente')

    list_filter = ('agenda',)

    def data(self, obj):
        return obj.agenda.dia

    def medico(self, obj):
        return obj.agenda.medico

    def paciente(self, obj):
        if obj.consultas.first():
            return obj.consultas.first().paciente
        else:
            return '-'

admin.site.register(Horario, HorarioAdmin)

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'horario', 'data_agendamento')
    list_filter = ('paciente',)
admin.site.register(Consulta, ConsultaAdmin)