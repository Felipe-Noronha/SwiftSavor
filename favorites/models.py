from django.db import models
from django.contrib.auth.models import User
from recipes.models import Receita

class ReceitaFavorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'receita')

    def __str__(self):
        return f"{self.usuario.username} - {self.receita.nome}"
