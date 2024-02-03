from django.db import models
from django.contrib.auth.models import User
from ingredients.models import Ingrediente
from django.utils import timezone

class Receita(models.Model):
    nome = models.CharField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente)
    instrucoes = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_cadastro = models.DateField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.nome
    

class ImagemReceita(models.Model):
    receita = models.ForeignKey(Receita, related_name='imagens_receita', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='receitas/')

    def __str__(self):
        return f"Imagem para {self.receita.nome}"
    

