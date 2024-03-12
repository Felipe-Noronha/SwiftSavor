from django.db import models
from django.contrib.auth.models import User
from ingredients.models import Ingrediente
from django.utils import timezone

class Receita(models.Model):
    nome = models.CharField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente)
    instruções = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_cadastro = models.DateField(auto_now_add=False, default=timezone.now)
    aprovada = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    

class ImagemReceita(models.Model):
    receita = models.ForeignKey(Receita, related_name='imagens_receita', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='receitas/', null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Imagem para {self.receita.nome}"
    

