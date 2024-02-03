from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Ingrediente(models.Model):
    nome = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.nome

class UsuarioIngrediente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    class Meta:
        unique_together = ('usuario', 'ingrediente')

    def __str__(self):
        return f"{self.usuario.username} - {self.ingrediente.nome}"
