from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html', {})

def configuracoes(request):
    return render(request, 'main/configuracoes.html')