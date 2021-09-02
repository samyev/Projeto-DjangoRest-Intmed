from django.db import models

# Create your models here.

class Especialidade(models.Model):
    nome = models.CharField(max_length=50, blank=False, verbose_name="Especialidade")

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    crm = models.IntegerField(blank=False, unique=True)
    email = models.CharField(max_length=255, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True)
    especialidade = models.ForeignKey(
      "Especialidade", 
      on_delete=models.DO_NOTHING, 
      null=True, 
      blank=True
    )


    def __str__(self):
        return self.nome