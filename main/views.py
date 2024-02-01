from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import ImagemReceita, Receita, Ingrediente, ReceitaFavorita, UsuarioIngrediente
from .forms import ImagemReceitaFormSet, ReceitaForm,IngredienteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User


def is_admin(user):
    return user.is_authenticated and user.is_staff

def index(request):
    return render(request, 'main/index.html', {})

@login_required
def lista_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'main/lista_receitas.html', {'receitas': receitas})

@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        formset = ImagemReceitaFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user  # Atribui o usuário logado à receita antes de salvá-la
            receita.save()
            form.save_m2m()  # Salva as relações ManyToMany depois de salvar o objeto principal

            for form_imagem in formset.cleaned_data:
                imagem = form_imagem.get('imagem')  # Obtenha a imagem a partir do formset
                if imagem:  # Verifique se a imagem existe antes de tentar salvar
                    ImagemReceita.objects.create(receita=receita, imagem=imagem)

            messages.success(request, 'Receita cadastrada com sucesso!')
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()
        formset = ImagemReceitaFormSet(queryset=ImagemReceita.objects.none())

    return render(request, 'main/cadastrar_receita.html', {'form': form, 'formset': formset})



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

@login_required
def editar_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    if request.user != ingrediente.usuario and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar este ingrediente.')
        return redirect('lista_ingredientes')
    else:
        form = IngredienteForm(instance=ingrediente)
    
    return render(request, 'main/editar_ingrediente.html', {'form': form, 'ingrediente': ingrediente})

@login_required
def excluir_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    if request.user != ingrediente.usuario and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para excluir este ingrediente.')
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
    pagina_atual = request.META.get('HTTP_REFERER')  # Obtém a URL da página anterior

    if ReceitaFavorita.objects.filter(usuario=request.user, receita=receita).exists():
        messages.warning(request, 'Esta receita já está nos seus favoritos.')
    else:
        ReceitaFavorita.objects.create(usuario=request.user, receita=receita)
        messages.success(request, f'Receita "{receita.nome}" adicionada aos favoritos com sucesso!')

    # Redireciona o usuário de volta para a página de onde veio
    return redirect(pagina_atual) if pagina_atual else redirect('lista_receitas')

def remover_favorito(request, receita_id):
    receita_favorita = get_object_or_404(ReceitaFavorita, receita__id=receita_id, usuario=request.user)
    receita_favorita.delete()
    return redirect('receitas_favoritas')


@user_passes_test(is_admin)
def admin_dashboard(request):
    # Lógica da view (se necessário)
    return render(request, 'main/admin_dashboard.html')


@login_required
def selecionar_ingredientes(request):
    usuario_ingredientes = UsuarioIngrediente.objects.filter(usuario=request.user).values_list('ingrediente_id', flat=True)

    if request.method == 'POST':
        ingrediente_id_para_adicionar = request.POST.get('ingrediente_id')
        if ingrediente_id_para_adicionar:
            _, created = UsuarioIngrediente.objects.get_or_create(
                usuario=request.user,
                ingrediente_id=ingrediente_id_para_adicionar
            )
            if created:
                messages.success(request, 'Ingrediente adicionado com sucesso.')
            return redirect('selecionar_ingredientes')

    query = request.GET.get('q', '')
    ingredientes = Ingrediente.objects.filter(nome__icontains=query) if query else Ingrediente.objects.all()

    return render(request, 'main/selecionar_ingredientes.html', {
        'ingredientes': ingredientes,
        'usuario_ingredientes': usuario_ingredientes,
        'query': query
    })


@login_required
def buscar_receitas_com_ingredientes(request):
    ingredientes_usuario = Ingrediente.objects.filter(usuario=request.user, selecionado=True)
    receitas = Receita.objects.filter(ingredientes__in=ingredientes_usuario).distinct()
    return render(request, 'main/buscar_receitas.html', {'receitas': receitas})

    
    
@login_required
def meus_ingredientes(request):
    usuario_ingredientes = UsuarioIngrediente.objects.filter(usuario=request.user)
    ingredientes = [ui.ingrediente for ui in usuario_ingredientes]

    # Lógica de remoção baseada em uma ação de POST
    if request.method == 'POST':
        ingrediente_id_para_remover = request.POST.get('ingrediente_id')
        if ingrediente_id_para_remover:
            UsuarioIngrediente.objects.filter(
                usuario=request.user, 
                ingrediente_id=ingrediente_id_para_remover
            ).delete()
            return redirect('meus_ingredientes')

    return render(request, 'main/meus_ingredientes.html', {'ingredientes_selecionados': ingredientes})


@login_required
def adicionar_ingrediente_usuario(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            novo_ingrediente = form.save(commit=False)
            novo_ingrediente.usuario = request.user  # Atribui o ingrediente ao usuário logado
            novo_ingrediente.save()
            messages.success(request, 'Ingrediente adicionado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm()
    return render(request, 'main/adicionar_ingrediente_usuario.html', {'form': form})


@login_required
def editar_ingrediente_usuario(request, usuario_ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=usuario_ingrediente_id, usuario=request.user)  # Certifique-se de ajustar este código conforme seu modelo

    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente atualizado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm(instance=ingrediente)

    return render(request, 'main/editar_ingrediente_usuario.html', {'form': form, 'ingrediente': ingrediente})


@login_required
def excluir_ingrediente_usuario(request, usuario_ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=usuario_ingrediente_id, usuario=request.user)
    if request.method == 'POST':
        ingrediente.delete()
        messages.success(request, 'Ingrediente excluído com sucesso!')
        return redirect('lista_ingredientes')
    else:
        return render(request, 'main/confirmar_exclusao_ingrediente.html', {'ingrediente': ingrediente})



def gestao_usuarios(request):
    # Verifica se o usuário atual é um administrador
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('index')
    
    # Lista todos os usuários
    usuarios = User.objects.all()

    return render(request, 'main/gestao_usuarios.html', {'usuarios': usuarios})

@login_required
def tornar_administrador(request, usuario_id):
    # Verifica se o usuário atual é um administrador
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
        return redirect('index')

    # Obtém o usuário com base no ID fornecido
    usuario = get_object_or_404(User, id=usuario_id)

    # Torna o usuário um administrador (altera a propriedade is_staff)
    usuario.is_staff = True
    usuario.save()

    messages.success(request, f'O usuário "{usuario.username}" agora é um administrador.')

    return redirect('gestao_usuarios')

@login_required
def excluir_usuario(request, usuario_id):
    # Verifica se o usuário atual é um administrador
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
        return redirect('index')

    # Obtém o usuário com base no ID fornecido
    usuario = get_object_or_404(User, id=usuario_id)

    # Verifica se o usuário não está tentando excluir a si mesmo
    if usuario == request.user:
        messages.error(request, 'Você não pode excluir a si mesmo.')
        return redirect('gestao_usuarios')

    # Remove o usuário do banco de dados
    usuario.delete()

    messages.success(request, f'O usuário "{usuario.username}" foi excluído com sucesso.')

    return redirect('gestao_usuarios')


@login_required
def remover_administrador(request, usuario_id):
    # Verifique se o usuário logado é um administrador
    if not request.user.is_staff:
        # Se não for administrador, redirecione ou mostre uma mensagem de erro
        # Redirecionamento de exemplo:
        return redirect('admin_dashboard')
    
    # Encontre o usuário pelo ID
    try:
        usuario = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        # Trate o caso em que o usuário não existe
        # Pode redirecionar ou mostrar uma mensagem de erro
        pass

    # Remova as permissões de administrador do usuário
    usuario.is_staff = False
    usuario.save()

    # Redirecione para a página de administração
    return redirect('gestao_usuarios')


@login_required
def receitas_recomendadas(request):
    # Primeiro, obtenha todos os IDs dos ingredientes que o usuário selecionou.
    ingredientes_usuario_ids = UsuarioIngrediente.objects.filter(
        usuario=request.user
    ).values_list('ingrediente_id', flat=True)

    # Em seguida, encontre as receitas que contêm pelo menos um dos ingredientes do usuário.
    # Note que isso pode retornar receitas para as quais o usuário não tem todos os ingredientes.
    receitas_possiveis = Receita.objects.filter(
        ingredientes__id__in=ingredientes_usuario_ids
    ).distinct()

    # Agora, filtre essas receitas para encontrar apenas aquelas para as quais o usuário tem todos os ingredientes.
    receitas_completas = []
    for receita in receitas_possiveis:
        ingredientes_receita_ids = set(receita.ingredientes.values_list('id', flat=True))
        if ingredientes_receita_ids.issubset(ingredientes_usuario_ids):
            receitas_completas.append(receita)

    return render(request, 'main/receitas_recomendadas.html', {'receitas': receitas_completas})
