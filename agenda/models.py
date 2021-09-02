from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from medicos.models import Medico

import datetime

# Create your models here.

class Agenda(models.Model):

  def validate_date(date):
    if date < datetime.date.today():
      raise ValidationError("Não é possível criar uma agenda para a data respectiva!")

  dia = models.DateField(blank=False, default=datetime.date.today, validators=[validate_date])
  medico = models.ForeignKey(Medico, blank=False, on_delete=models.CASCADE)
  
  class Meta:
    verbose_name = "Agenda"
    verbose_name_plural = "Agendas"
    unique_together = ('medico', 'dia')
  
  def __str__(self):
        return f'{self.medico} - {self.dia.strftime("%d/%m/%Y")}'
  

class Horario(models.Model):
  agenda = models.ForeignKey(Agenda, blank=False, on_delete=models.CASCADE, related_name="horarios")
  horario = models.TimeField(null=False, blank=False)

  class Meta:
    verbose_name = "Horário"
    verbose_name_plural = "Horários"
    unique_together = ("agenda", "hora")
  
  def __str__(self):
        return self.hora.strftime('%H:%M')


class Consulta(models.Model):
    dia = models.ForeignKey(User, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, blank=False, on_delete=models.CASCADE, related_name='consultas')
    data_agendamento = models.DateTimeField(auto_now_add=True)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

    def medico(self):
        return self.horario.agenda.medico

    class Meta:
        ordering = ['horario']
        unique_together = ('data_agendamento', 'horario')

    def __str__(self):
        return self.paciente.__str__() + ' - ' + self.horario.__str__()