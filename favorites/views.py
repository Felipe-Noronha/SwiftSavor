from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from recipes.models import Receita
from .models import ReceitaFavorita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def adicionar_favoritos(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    pagina_atual = request.META.get('HTTP_REFERER')

    if ReceitaFavorita.objects.filter(usuario=request.user, receita=receita).exists():
        messages.warning(request, 'Esta receita já está nos seus favoritos.')
    else:
        ReceitaFavorita.objects.create(usuario=request.user, receita=receita)
        messages.success(request, f'Receita "{receita.nome}" adicionada aos favoritos com sucesso!')

    return redirect(pagina_atual) if pagina_atual else redirect(reverse('recipes:lista_receitas'))

@login_required
def remover_favorito(request, receita_id):
    receita_favorita = get_object_or_404(ReceitaFavorita, receita__id=receita_id, usuario=request.user)
    pagina_atual = request.META.get('HTTP_REFERER')
    receita_favorita.delete()
    messages.success(request, 'Receita removida dos favoritos com sucesso.')
    return redirect(pagina_atual) if pagina_atual else redirect(reverse('recipes:lista_receitas'))

@login_required
def receitas_favoritas(request):
    receitas_favoritas = ReceitaFavorita.objects.filter(usuario=request.user).select_related('receita')

    paginator = Paginator(receitas_favoritas, 10)
    page = request.GET.get('page')

    try:
        receitas_favoritas = paginator.page(page)
    except PageNotAnInteger:
        receitas_favoritas = paginator.page(1)
    except EmptyPage:
        receitas_favoritas = paginator.page(paginator.num_pages)

    return render(request, 'favorites/receitas_favoritas.html', {'receitas_favoritas': receitas_favoritas})
