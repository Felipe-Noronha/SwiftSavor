from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from recipes.models import Receita
from .models import ReceitaFavorita

@login_required
def adicionar_favoritos(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    pagina_atual = request.META.get('HTTP_REFERER')

    if ReceitaFavorita.objects.filter(usuario=request.user, receita=receita).exists():
        messages.warning(request, 'Esta receita já está nos seus favoritos.')
    else:
        ReceitaFavorita.objects.create(usuario=request.user, receita=receita)
        messages.success(request, f'Receita "{receita.nome}" adicionada aos favoritos com sucesso!')

    return redirect(pagina_atual) if pagina_atual else redirect('recipes:lista_receitas')

@login_required
def remover_favorito(request, receita_id):
    receita_favorita = get_object_or_404(ReceitaFavorita, receita__id=receita_id, usuario=request.user)
    receita_favorita.delete()
    messages.success(request, 'Receita removida dos favoritos com sucesso.')
    return redirect('favorites:receitas_favoritas')

@login_required
def receitas_favoritas(request):
    receitas_favoritas = ReceitaFavorita.objects.filter(usuario=request.user).select_related('receita')
    return render(request, 'favorites/receitas_favoritas.html', {'receitas_favoritas': receitas_favoritas})
