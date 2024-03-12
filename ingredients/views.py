from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Ingrediente, UsuarioIngrediente
from .forms import IngredienteForm



def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def cadastrar_ingrediente(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            ingrediente = form.save(commit=False)
            ingrediente.user = request.user
            ingrediente.save()
            messages.success(request, 'Ingrediente cadastrado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm()

    return render(request, 'ingredients/cadastrar_ingrediente.html', {'form': form})


def lista_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'ingredients/lista_ingredientes.html', {'ingredientes': ingredientes})


@login_required
def editar_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    
    if request.user != ingrediente.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar este ingrediente.')
        return redirect('lista_ingredientes')
    
    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente atualizado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm(instance=ingrediente)
    
    return render(request, 'ingredients/editar_ingrediente.html', {'form': form, 'ingrediente': ingrediente})



@login_required
def excluir_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, pk=ingrediente_id)
    usuario_ingrediente = UsuarioIngrediente.objects.filter(usuario=request.user, ingrediente=ingrediente).exists()

    if usuario_ingrediente or request.user.is_staff:
        ingrediente.delete()
        return redirect('lista_ingredientes')
    else:
        messages.error(request, 'Você não tem permissão para excluir este ingrediente.')
        return redirect('lista_ingredientes')




def detalhes_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    context = {
        'ingrediente': ingrediente,
    }
    return render(request, 'ingredients/detalhes_ingrediente.html', context)


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
    ingredientes = Ingrediente.objects.filter(nome__icontains=query).order_by('nome') if query else Ingrediente.objects.all().order_by('nome')

    return render(request, 'ingredients/selecionar_ingredientes.html', {
        'ingredientes': ingredientes,
        'usuario_ingredientes': usuario_ingredientes,
        'query': query
    })


@login_required
def meus_ingredientes(request):
    usuario_ingredientes = UsuarioIngrediente.objects.filter(usuario=request.user)
    ingredientes = [ui.ingrediente for ui in usuario_ingredientes]
    ingredientes_selecionados = sorted(ingredientes, key=lambda x: x.nome)

    if request.method == 'POST':
        ingrediente_id_para_remover = request.POST.get('ingrediente_id')
        if ingrediente_id_para_remover:
            UsuarioIngrediente.objects.filter(
                usuario=request.user, 
                ingrediente_id=ingrediente_id_para_remover
            ).delete()
            return redirect('meus_ingredientes')

    return render(request, 'ingredients/meus_ingredientes.html', {'ingredientes_selecionados': ingredientes_selecionados})




@login_required
def adicionar_ingrediente_usuario(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            novo_ingrediente = form.save(commit=False)
            novo_ingrediente.usuario = request.user
            novo_ingrediente.save()
            messages.success(request, 'Ingrediente adicionado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm()
    return render(request, 'ingredients/adicionar_ingrediente_usuario.html', {'form': form})


@login_required
def editar_ingrediente_usuario(request, usuario_ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=usuario_ingrediente_id, usuario=request.user)

    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente atualizado com sucesso!')
            return redirect('lista_ingredientes')
    else:
        form = IngredienteForm(instance=ingrediente)

    return render(request, 'ingredients/editar_ingrediente_usuario.html', {'form': form, 'ingrediente': ingrediente})


@login_required
def excluir_ingrediente_usuario(request, usuario_ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=usuario_ingrediente_id, usuario=request.user)
    if request.method == 'POST':
        ingrediente.delete()
        messages.success(request, 'Ingrediente excluído com sucesso!')
        return redirect('lista_ingredientes')
    else:
        return render(request, 'ingredients/confirmar_exclusao_ingrediente.html', {'ingrediente': ingrediente})
    

    