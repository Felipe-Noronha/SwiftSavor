from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Receita
from .forms import ReceitaForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/index.html', {})

@login_required
def lista_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'main/lista_receitas.html', {'receitas': receitas})

@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()

    return render(request, 'main/cadastrar_receita.html', {'form': form})

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'main/cadastrar_usuario.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('index')