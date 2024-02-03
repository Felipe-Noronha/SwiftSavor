from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('gestao/', views.gestao_usuarios, name='gestao_usuarios'),
    path('tornar_admin/<int:usuario_id>/', views.tornar_administrador, name='tornar_administrador'),
    path('excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('remover_admin/<int:usuario_id>/', views.remover_administrador, name='remover_administrador'),
    path('trocar_email/', views.trocar_email, name='trocar_email'),
    path('trocar_senha/', views.trocar_senha, name='trocar_senha'),
]
