# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone

class Ingrediente(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    
class UsuarioIngrediente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)  # Opcional, se você quiser rastrear a quantidade

    class Meta:
        unique_together = ('usuario', 'ingrediente')  # Isso garante que o par usuário-ingrediente seja único

    def __str__(self):
        return f"{self.usuario.username} - {self.ingrediente.nome}"    

class Receita(models.Model):
    nome = models.CharField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente)
    instrucoes = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # O usuário que criou a receita
    data_cadastro = models.DateField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.nome

class ReceitaFavorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'receita')  # Isso garante que o par usuário-receita seja único

    def __str__(self):
        return f"{self.usuario.username} - {self.receita.nome}"