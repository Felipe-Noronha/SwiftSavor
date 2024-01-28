from django.db import models
from django.contrib.auth.models import AbstractUser

class Receita(models.Model):
    nome = models.CharField(max_length=200)
    ingredientes = models.TextField()
    instrucoes = models.TextField()

    def __str__(self):
        return self.nome