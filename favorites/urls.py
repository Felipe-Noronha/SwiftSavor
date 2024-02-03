from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('adicionar/<int:receita_id>/', views.adicionar_favoritos, name='adicionar_favoritos'),
    path('remover/<int:receita_id>/', views.remover_favorito, name='remover_favorito'),
    path('favoritas/', views.receitas_favoritas, name='receitas_favoritas'),
]
