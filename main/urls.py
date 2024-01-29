from django.urls import path
from . import views
from .views import (cadastrar_receita,
                    index,
                    lista_receitas,
                    cadastrar_usuario, 
                    logout_usuario, 
                    detalhes_receita,
                    cadastrar_ingrediente, 
                    receitas_favoritas, 
                    adicionar_favoritos, 
                    remover_favorito, 
                    excluir_receita, 
                    editar_receita, 
                    admin_dashboard,
                    lista_ingredientes,
                    editar_ingrediente,
                    excluir_ingrediente,
                    selecionar_ingredientes,
                    meus_ingredientes,
                    )
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', index, name='index'),
    path('receitas/', lista_receitas, name='lista_receitas'),
    path('receitas/cadastrar/', cadastrar_receita, name='cadastrar_receita'),
    path('receitas/<int:receita_id>/', detalhes_receita, name='detalhes_receita'),
    path('receitas_favoritas/', receitas_favoritas, name='receitas_favoritas'),
    path('excluir_receita/<int:receita_id>/', excluir_receita, name='excluir_receita'),
    path('editar_receita/<int:receita_id>/', editar_receita, name='editar_receita'),

    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', logout_usuario, name='logout'),

    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    
    path('cadastrar_ingrediente/', cadastrar_ingrediente, name='cadastrar_ingrediente'),
    path('lista_ingredientes/', lista_ingredientes, name='lista_ingredientes'),
    path('editar_ingrediente/<int:ingrediente_id>/', editar_ingrediente, name='editar_ingrediente'),
    path('excluir_ingrediente/<int:ingrediente_id>/', excluir_ingrediente, name='excluir_ingrediente'),
    path('detalhes_ingrediente/<int:ingrediente_id>/', views.detalhes_ingrediente, name='detalhes_ingrediente'),
    path('selecionar_ingredientes/', selecionar_ingredientes, name='selecionar_ingredientes'),
    path('meus_ingredientes/<str:ingredientes_ids>/', meus_ingredientes, name='meus_ingredientes'),
    path('meus_ingredientes/', meus_ingredientes, name='meus_ingredientes'),

    path('adicionar_favoritos/<int:receita_id>/', adicionar_favoritos, name='adicionar_favoritos'),
    path('remover_favorito/<int:receita_id>/', remover_favorito, name='remover_favorito'),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
]
