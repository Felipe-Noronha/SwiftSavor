# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Ingrediente(models.Model):
    nome = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    selecionado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Receita(models.Model):
    nome = models.CharField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente)
    instrucoes = models.TextField()

    def __str__(self):
        return self.nome

class ReceitaFavorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.username} - {self.receita.nome}"