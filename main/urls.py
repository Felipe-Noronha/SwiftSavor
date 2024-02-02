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
                    buscar_receitas_com_ingredientes,
                    receitas_recomendadas,
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
    path('meus_ingredientes/', views.meus_ingredientes, name='meus_ingredientes'),
    path('buscar_receitas_com_ingredientes/', buscar_receitas_com_ingredientes, name='buscar_receitas_com_ingredientes'),
    path('adicionar_ingrediente_usuario/', views.adicionar_ingrediente_usuario, name='adicionar_ingrediente_usuario'),
    path('editar_ingrediente_usuario/<int:usuario_ingrediente_id>/', views.editar_ingrediente_usuario, name='editar_ingrediente_usuario'),
    path('excluir_ingrediente_usuario/<int:usuario_ingrediente_id>/', views.excluir_ingrediente_usuario, name='excluir_ingrediente_usuario'),


    path('adicionar_favoritos/<int:receita_id>/', adicionar_favoritos, name='adicionar_favoritos'),
    path('remover_favorito/<int:receita_id>/', remover_favorito, name='remover_favorito'),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    path('gestao_usuarios/', views.gestao_usuarios, name='gestao_usuarios'),

    path('tornar_administrador/<int:usuario_id>/', views.tornar_administrador, name='tornar_administrador'),

    path('excluir_usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),

    path('remover_administrador/<int:usuario_id>/', views.remover_administrador, name='remover_administrador'),
    path('receitas_recomendadas/', receitas_recomendadas, name='receitas_recomendadas'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),

    path('trocar_email/', views.trocar_email, name='trocar_email'),
    path('trocar_senha/', views.trocar_senha, name='trocar_senha'),

]
