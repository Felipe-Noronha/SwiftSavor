from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ChangeEmailForm, ChangePasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash





def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/cadastrar_usuario.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('index')

def gestao_usuarios(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('index')
    
    usuarios = User.objects.all()

    return render(request, 'users/gestao_usuarios.html', {'usuarios': usuarios})



@login_required
def tornar_administrador(request, usuario_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
        return redirect('index')

    usuario = get_object_or_404(User, id=usuario_id)
    usuario.is_staff = True
    usuario.save()

    messages.success(request, f'O usuário "{usuario.username}" agora é um administrador.')

    return redirect('gestao_usuarios')


@login_required
def excluir_usuario(request, usuario_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
        return redirect('index')

    usuario = get_object_or_404(User, id=usuario_id)

    if usuario == request.user:
        messages.error(request, 'Você não pode excluir a si mesmo.')
        return redirect('gestao_usuarios')

    usuario.delete()

    messages.success(request, f'O usuário "{usuario.username}" foi excluído com sucesso.')

    return redirect('gestao_usuarios')


@login_required
def remover_administrador(request, usuario_id):
    if not request.user.is_staff:
        return redirect('admin_dashboard')
    
    try:
        usuario = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        pass

    usuario.is_staff = False
    usuario.save()

    return redirect('gestao_usuarios')

@login_required
def trocar_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()
            return redirect('configuracoes')
    else:
        form = ChangeEmailForm()

    return render(request, 'users/trocar_email.html', {'form': form})



@login_required
def trocar_senha(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('configuracoes')
        else:
            messages.error(request, 'Houve um erro ao alterar sua senha. Por favor, corrija os erros abaixo.')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'users/trocar_senha.html', {'form': form})
