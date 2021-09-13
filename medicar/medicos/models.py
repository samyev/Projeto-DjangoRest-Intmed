from django.db import models

class Especialidade(models.Model):
    nome = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=255, blank=False)
    crm = models.IntegerField(blank=True, unique=True)
    email = models.CharField(max_length=255, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.nome