from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ingredientes, name='lista_ingredientes'),
    path('cadastrar/', views.cadastrar_ingrediente, name='cadastrar_ingrediente'),
    path('editar/<int:ingrediente_id>/', views.editar_ingrediente, name='editar_ingrediente'),
    path('excluir/<int:ingrediente_id>/', views.excluir_ingrediente, name='excluir_ingrediente'),
    path('selecionar/', views.selecionar_ingredientes, name='selecionar_ingredientes'),
    path('meus/', views.meus_ingredientes, name='meus_ingredientes'),
    path('adicionar_usuario/', views.adicionar_ingrediente_usuario, name='adicionar_ingrediente_usuario'),
    path('editar_usuario/<int:usuario_ingrediente_id>/', views.editar_ingrediente_usuario, name='editar_ingrediente_usuario'),
    path('detalhes_ingrediente/<int:ingrediente_id>/', views.detalhes_ingrediente, name='detalhes_ingrediente'),
    path('excluir_usuario/<int:usuario_ingrediente_id>/', views.excluir_ingrediente_usuario, name='excluir_ingrediente_usuario'),
]
