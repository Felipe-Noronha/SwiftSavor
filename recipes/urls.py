from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_receitas, name='lista_receitas'),
    path('cadastrar/', views.cadastrar_receita, name='cadastrar_receita'),
    path('<int:receita_id>/', views.detalhes_receita, name='detalhes_receita'),
    path('excluir/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),
    path('editar/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('recomendadas/', views.receitas_recomendadas, name='receitas_recomendadas'),
    path('compartilhar/<int:receita_id>/', views.compartilhar_receita, name='compartilhar_receita'),
    path('aprovar_receita/<int:receita_id>/', views.aprovar_receita, name='aprovar_receita'),
    path('receitas_pendentes/', views.lista_pendentes, name='lista_pendentes'),
]
