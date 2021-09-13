from django.db import models
from django.contrib.auth.models import User
from medicos.models import Medico
import datetime
from django.core.exceptions import ValidationError

class Agenda(models.Model):
    def validate_date(date):
        if date < datetime.date.today():
            raise ValidationError("Data inválida!")
            
    medico = models.ForeignKey(Medico, blank=False, on_delete=models.CASCADE)
    dia = models.DateField(blank=False, default=datetime.date.today, validators=[validate_date])

    def get_dia(self):
        return str(self.dia.strftime("%Y-%m-%d"))

    def __str__(self):
        return self.medico.nome + ' - ' + str(self.dia.strftime("%d/%m/%Y"))

    class Meta:
        ordering = ['dia']
        unique_together = ('dia', 'medico')


class Horario(models.Model):
    horario = models.TimeField(blank=False)
    agenda = models.ForeignKey(Agenda, blank=False, on_delete=models.CASCADE, related_name='horarios')

    def get_horario(self):
        return self.horario.strftime("%H:%M")
        
    def __str__(self):
        return self.get_horario() + ' - ' + self.agenda.__str__()

    class Meta:
        ordering = ['agenda_dia','horario']

class Consulta(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    horario = models.ForeignKey(Horario, blank=False, on_delete=models.CASCADE, related_name='consultas')

    def medico(self):
        return self.horario.agenda.medico

    class Meta:
        ordering = ['horario']
        unique_together = ('data_agendamento', 'horario')

    def __str__(self):
        return self.paciente.__str__() + ' - ' + self.horario.__str__()

