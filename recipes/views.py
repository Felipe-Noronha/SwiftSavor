from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Receita, ImagemReceita
from .forms import EditarImagemReceitaForm, EditarReceitaForm, PesquisaReceitaForm, ReceitaForm, ImagemReceitaFormSet
from ingredients.models import Ingrediente,UsuarioIngrediente
from urllib.parse import quote
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from favorites.models import ReceitaFavorita
from django.forms import modelformset_factory
from django.forms import inlineformset_factory


@login_required
def lista_receitas(request):
    form_pesquisa = PesquisaReceitaForm(request.GET)
    receitas = Receita.objects.filter(aprovada=True)

    if form_pesquisa.is_valid():
        termo_pesquisa = form_pesquisa.cleaned_data['pesquisa']
        receitas = receitas.filter(nome__icontains=termo_pesquisa)

    receitas = receitas.order_by('nome')

    if request.user.is_authenticated:
        receitas_favoritas_ids = list(
            ReceitaFavorita.objects.filter(usuario=request.user).values_list('receita__id', flat=True)
        )
    else:
        receitas_favoritas_ids = []

    paginator = Paginator(receitas, 10)
    page = request.GET.get('page')

    try:
        receitas = paginator.page(page)
    except PageNotAnInteger:
        receitas = paginator.page(1)
    except EmptyPage:
        receitas = paginator.page(paginator.num_pages)

    return render(request, 'recipes/lista_receitas.html', {'receitas': receitas, 'form_pesquisa': form_pesquisa, 'receitas_favoritas_ids': receitas_favoritas_ids})


@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        formset = ImagemReceitaFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.aprovada = False
            receita.save()
            form.save_m2m()

            for form_imagem in formset.cleaned_data:
                imagem = form_imagem.get('imagem')
                url = form_imagem.get('url')
                if imagem:
                    ImagemReceita.objects.create(receita=receita, imagem=imagem)
                elif url:
                    ImagemReceita.objects.create(receita=receita, url=url)    

            messages.success(request, 'Receita cadastrada com sucesso! Aguardando aprovação.')
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()
        formset = ImagemReceitaFormSet(queryset=ImagemReceita.objects.none())

    return render(request, 'recipes/cadastrar_receita.html', {'form': form, 'formset': formset})


@login_required
def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    ImagemReceitaFormSet = inlineformset_factory(Receita, ImagemReceita, form=EditarImagemReceitaForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = EditarReceitaForm(request.POST, instance=receita)
        formset_imagem = ImagemReceitaFormSet(request.POST, request.FILES, instance=receita)

        if form.is_valid() and formset_imagem.is_valid():
            form.save()
            formset_imagem.save()
            messages.success(request, 'Receita editada com sucesso.')
            return redirect('detalhes_receita', receita_id=receita_id)
    else:
        form = EditarReceitaForm(instance=receita)
        formset_imagem = ImagemReceitaFormSet(instance=receita)

    return render(request, 'recipes/editar_receita.html', {'form': form, 'formset_imagem': formset_imagem, 'receita': receita})




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
        ingredientes__id__in=ingredientes_usuario_ids,
        aprovada=True
    ).distinct()

    receitas_completas = []
    for receita in receitas_possiveis:
        ingredientes_receita_ids = set(receita.ingredientes.values_list('id', flat=True))
        if ingredientes_receita_ids.issubset(ingredientes_usuario_ids):
            receitas_completas.append(receita)

    paginator = Paginator(receitas_completas, 10)
    page = request.GET.get('page')

    try:
        receitas = paginator.page(page)
    except PageNotAnInteger:
        receitas = paginator.page(1)
    except EmptyPage:
        receitas = paginator.page(paginator.num_pages)

    receitas_favoritas_ids = list(
        ReceitaFavorita.objects.filter(usuario=request.user).values_list('receita__id', flat=True)
    )

    return render(request, 'recipes/receitas_recomendadas.html', {'receitas': receitas, 'receitas_favoritas_ids': receitas_favoritas_ids})

@login_required
def compartilhar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    link_unido = request.build_absolute_uri(reverse('detalhes_receita', args=[receita_id]))
    link_whatsapp = f'https://api.whatsapp.com/send?text={quote(link_unido)}'

    return render(request, 'recipes/compartilhar_receita.html', {'receita': receita, 'link_whatsapp': link_whatsapp})



@user_passes_test(lambda u: u.is_staff, login_url='index')
def aprovar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    
    if request.method == 'POST':
        receita.aprovada = True
        receita.save()
        messages.success(request, 'Receita aprovada com sucesso.')
        return redirect('lista_pendentes')

    return render(request, 'recipes/detalhes_receita.html', {'receita': receita})


@user_passes_test(lambda u: u.is_staff, login_url='index')
def lista_pendentes(request):
    receitas_pendentes = Receita.objects.filter(aprovada=False)
    return render(request, 'recipes/lista_pendentes.html', {'receitas_pendentes': receitas_pendentes})