from django.urls import path
from .views import cadastrar_receita, index, lista_receitas, cadastrar_usuario, logout_usuario
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', index, name='index'),
    path('receitas/', lista_receitas, name='lista_receitas'),
    path('receitas/cadastrar/', cadastrar_receita, name='cadastrar_receita'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
]
