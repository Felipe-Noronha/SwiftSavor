from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_receitas, name='lista_receitas'),
    path('cadastrar/', views.cadastrar_receita, name='cadastrar_receita'),
    path('<int:receita_id>/', views.detalhes_receita, name='detalhes_receita'),
    path('excluir/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),
    path('editar/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('recomendadas/', views.receitas_recomendadas, name='receitas_recomendadas'),
]
