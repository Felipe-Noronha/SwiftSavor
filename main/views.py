from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Receita, Ingrediente, ReceitaFavorita
from .forms import ReceitaForm,IngredienteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse


def is_admin(user):
    return user.is_authenticated and user.is_staff

def index(request):
    return render(request, 'main/index.html', {})

@login_required
def lista_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'main/lista_receitas.html', {'receitas': receitas})

@user_passes_test(is_admin)
def cadastrar_receita(request):
    ingredientes = Ingrediente.objects.all()
    
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()

    return render(request, 'main/cadastrar_receita.html', {'form': form, 'ingredientes': ingredientes})


def editar_receita(request, receita_id):
    # Verifica se o usuário está autenticado e é um administrador
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('lista_receitas')

    receita = get_object_or_404(Receita, pk=receita_id)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receita editada com sucesso!')
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(instance=receita)

    return render(request, 'main/editar_receita.html', {'form': form})

@user_passes_test(lambda u: u.is_staff, login_url='index')
def excluir_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso.')
        return redirect('lista_receitas')
    return render(request, 'main/excluir_receita.html', {'receita': receita})

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

def detalhes_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    return render(request, 'main/detalhes_receita.html', {'receita': receita})

@user_passes_test(is_admin)
def cadastrar_ingrediente(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente cadastrado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm()

    return render(request, 'main/cadastrar_ingrediente.html', {'form': form})

def lista_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'main/lista_ingredientes.html', {'ingredientes': ingredientes})

@user_passes_test(is_admin)
def editar_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)

    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente editado com sucesso.')
            return redirect('lista_ingredientes')  # Alteração aqui
    else:
        form = IngredienteForm(instance=ingrediente)
    
    return render(request, 'main/editar_ingrediente.html', {'form': form, 'ingrediente': ingrediente})

@user_passes_test(is_admin)
def excluir_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    if request.method == 'POST':
        ingrediente.delete()
        messages.success(request, 'Ingrediente excluído com sucesso.')
        return redirect('lista_ingredientes')
    return render(request, 'main/excluir_ingrediente.html', {'ingrediente': ingrediente})


def detalhes_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    context = {
        'ingrediente': ingrediente,
    }
    return render(request, 'main/detalhes_ingrediente.html', context)



@login_required
def receitas_favoritas(request):
    receitas_favoritas = ReceitaFavorita.objects.filter(usuario=request.user)
    return render(request, 'main/receitas_favoritas.html', {'receitas_favoritas': receitas_favoritas})


@login_required
def adicionar_favoritos(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)

    if ReceitaFavorita.objects.filter(usuario=request.user, receita=receita).exists():
        messages.warning(request, 'Esta receita já está nos seus favoritos.')
    else:
        ReceitaFavorita.objects.create(usuario=request.user, receita=receita)
        messages.success(request, f'Receita "{receita.nome}" adicionada aos favoritos com sucesso!')
    return redirect('lista_receitas')

def remover_favorito(request, receita_id):
    receita_favorita = get_object_or_404(ReceitaFavorita, receita__id=receita_id, usuario=request.user)
    receita_favorita.delete()
    return redirect('receitas_favoritas')

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Lógica da view (se necessário)
    return render(request, 'main/admin_dashboard.html')


def selecionar_ingredientes(request):
    if request.method == 'POST':
        ingredientes_selecionados_ids = request.POST.getlist('ingredientes_selecionados')

        # Lógica para salvar os ingredientes selecionados (exemplo)
        for ingrediente_id in ingredientes_selecionados_ids:
            ingrediente = Ingrediente.objects.get(pk=ingrediente_id)
            ingrediente.selecionado = True
            ingrediente.save()

        # Atualize esta parte para a lógica desejada

        # Obtém a lista atualizada de ingredientes
        ingredientes = Ingrediente.objects.all()
        
        # Adiciona uma mensagem de sucesso (opcional)
        messages.success(request, 'Ingredientes selecionados foram salvos com sucesso.')

        # Renderiza a mesma página com a lista atualizada de ingredientes
        return render(request, 'main/selecionar_ingredientes.html', {'ingredientes': ingredientes})

    else:
        # Se for uma requisição GET, simplesmente exibe a página
        ingredientes = Ingrediente.objects.all()
        return render(request, 'main/selecionar_ingredientes.html', {'ingredientes': ingredientes})
    
    
@login_required
def meus_ingredientes(request):
    ingredientes_selecionados = Ingrediente.objects.filter(usuario=request.user, selecionado=True)
    return render(request, 'main/meus_ingredientes.html', {'ingredientes_selecionados': ingredientes_selecionados})