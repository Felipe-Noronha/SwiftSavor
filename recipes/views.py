from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Receita, ImagemReceita
from .forms import PesquisaReceitaForm, ReceitaForm, ImagemReceitaFormSet
from ingredients.models import Ingrediente,UsuarioIngrediente
from urllib.parse import quote
from django.urls import reverse


@login_required
def lista_receitas(request):
    form_pesquisa = PesquisaReceitaForm(request.GET)
    receitas = Receita.objects.all()

    if form_pesquisa.is_valid():
        termo_pesquisa = form_pesquisa.cleaned_data['pesquisa']
        receitas = receitas.filter(nome__icontains=termo_pesquisa)

    return render(request, 'recipes/lista_receitas.html', {'receitas': receitas, 'form_pesquisa': form_pesquisa})


@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        formset = ImagemReceitaFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.save()
            form.save_m2m()

            for form_imagem in formset.cleaned_data:
                imagem = form_imagem.get('imagem')
                if imagem:
                    ImagemReceita.objects.create(receita=receita, imagem=imagem)

            messages.success(request, 'Receita cadastrada com sucesso!')
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()
        formset = ImagemReceitaFormSet(queryset=ImagemReceita.objects.none())

    return render(request, 'recipes/cadastrar_receita.html', {'form': form, 'formset': formset})

def editar_receita(request, receita_id):
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

    return render(request, 'recipes/editar_receita.html', {'form': form})


@user_passes_test(lambda u: u.is_staff, login_url='index')
def excluir_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso.')
        return redirect('lista_receitas')
    return render(request, 'recipes/excluir_receita.html', {'receita': receita})


@login_required
def detalhes_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    ingredientes_usuario_ids = UsuarioIngrediente.objects.filter(
        usuario=request.user
    ).values_list('ingrediente_id', flat=True)
    
    ingredientes_faltando = receita.ingredientes.exclude(id__in=ingredientes_usuario_ids)

    return render(request, 'recipes/detalhes_receita.html', {'receita': receita, 'ingredientes_faltando': ingredientes_faltando})



@login_required
def receitas_recomendadas(request):
    ingredientes_usuario_ids = UsuarioIngrediente.objects.filter(
        usuario=request.user
    ).values_list('ingrediente_id', flat=True)

    receitas_possiveis = Receita.objects.filter(
        ingredientes__id__in=ingredientes_usuario_ids
    ).distinct()

    receitas_completas = []
    for receita in receitas_possiveis:
        ingredientes_receita_ids = set(receita.ingredientes.values_list('id', flat=True))
        if ingredientes_receita_ids.issubset(ingredientes_usuario_ids):
            receitas_completas.append(receita)

    return render(request, 'recipes/receitas_recomendadas.html', {'receitas': receitas_completas})


@login_required
def compartilhar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    link_unido = request.build_absolute_uri(reverse('detalhes_receita', args=[receita_id]))
    link_whatsapp = f'https://api.whatsapp.com/send?text={quote(link_unido)}'

    return render(request, 'recipes/compartilhar_receita.html', {'receita': receita, 'link_whatsapp': link_whatsapp})