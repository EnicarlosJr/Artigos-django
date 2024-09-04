from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import FileResponse, Http404
import mimetypes
import os
from .forms import ArtigoForm, ConfirmacaoExclusaoForm
from .models import Artigo
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, 'home.html')

def criar(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)  # Inclua request.FILES para lidar com uploads
        if form.is_valid():
            form.save()  # Salva o artigo e o arquivo
            return redirect('lista_artigos')  # Redireciona para a lista de artigos após o salvamento
    else:
        form = ArtigoForm()
    
    return render(request, 'criar.html', {'form': form})

def lista_artigos(request):
    # Obtém os filtros e a ordenação
    filtros = {
        'titulo': request.GET.get('titulo', ''),
        'autor': request.GET.get('autor', ''),
        'revista': request.GET.get('revista', ''),
        'palavra_chave': request.GET.get('palavra_chave', ''),
        'data': request.GET.get('data', ''),
        'resumo': request.GET.get('resumo', '')
    }
    
    ordenar_por = request.GET.get('ordenar_por', 'data')
    pagina = request.GET.get('pagina', 1)

    artigos = Artigo.objects.all()

    # Aplica os filtros
    if filtros['titulo']:
        artigos = artigos.filter(titulo__icontains=filtros['titulo'])
    if filtros['autor']:
        artigos = artigos.filter(autores__icontains=filtros['autor'])
    if filtros['revista']:
        artigos = artigos.filter(revista__icontains=filtros['revista'])
    if filtros['palavra_chave']:
        artigos = artigos.filter(palavras_chave__icontains=filtros['palavra_chave'])
    if filtros['data']:
        artigos = artigos.filter(data=filtros['data'])
    if filtros['resumo']:
        artigos = artigos.filter(resumo__icontains=filtros['resumo'])

    # Ordena os resultados
    artigos = artigos.order_by(ordenar_por)

    # Pagina os resultados
    paginator = Paginator(artigos, 10)  # 10 artigos por página
    artigos_paginados = paginator.get_page(pagina)

    return render(request, 'lista_artigos.html', {
        'artigos': artigos_paginados,
        'filtros': filtros,
        'ordenar_por': ordenar_por
    })

def editar(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)
    if request.method == 'POST':
        form = ArtigoForm(request.POST, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('detalhes_artigo', artigo_id=artigo_id)  # ou outra página de sucesso
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'editar.html', {'form': form, 'artigo': artigo})

def detalhes_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)
    return render(request, 'detalhes_artigo.html', {'artigo': artigo})


def download_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)

    # Verifica se o arquivo existe
    if artigo.arquivo and artigo.arquivo.storage.exists(artigo.arquivo.name):
        # Obtém o caminho absoluto do arquivo
        file_path = artigo.arquivo.path
        
        # Obtém o tipo MIME do arquivo
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Prepara a resposta para o arquivo
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        # Caso o arquivo não exista, renderiza um template de erro
        raise Http404("Arquivo não encontrado")
    
def excluir_artigo(request, artigo_id):
    # Obtém o objeto Artigo ou retorna 404 se não encontrado
    artigo = get_object_or_404(Artigo, pk=artigo_id)

    if artigo.arquivo:
        arquivo_path = artigo.arquivo.path
        
        if os.path.exists(arquivo_path):
            try:
                os.remove(arquivo_path)
            except OSError as e:
                print(f"Erro ao remover o arquivo: {e}")
                return redirect('lista_artigos')

        # Remove a referência ao arquivo do banco de dados, mas não salva o objeto ainda
        artigo.arquivo.delete(save=False)
        
        # Salva o artigo sem o arquivo associado
        artigo.save()

    # Remove o artigo do banco de dados
    artigo.delete()

    # Redireciona para a página de lista de artigos após a exclusão
    return redirect('lista_artigos')  

def busca_artigos(request):
    query = request.GET.get('q', '')
    filtros = {
        'titulo': request.GET.get('titulo', ''),
        'autor': request.GET.get('autor', ''),
        'revista': request.GET.get('revista', ''),
        'palavra_chave': request.GET.get('palavra_chave', ''),
        'data': request.GET.get('data', ''),
        'resumo': request.GET.get('resumo', '')
    }

    artigos = Artigo.objects.all()

    if filtros['titulo']:
        artigos = artigos.filter(titulo__icontains=filtros['titulo'])
    if filtros['autor']:
        artigos = artigos.filter(autor__icontains=filtros['autor'])
    if filtros['revista']:
        artigos = artigos.filter(revista__icontains=filtros['revista'])
    if filtros['palavra_chave']:
        artigos = artigos.filter(palavras_chave__icontains=filtros['palavra_chave'])
    if filtros['data']:
        artigos = artigos.filter(data_publicacao__date=filtros['data'])
    if filtros['resumo']:
        artigos = artigos.filter(resumo__icontains=filtros['resumo'])

    # Ordenação
    ordenar_por = request.GET.get('ordenar_por', 'data_publicacao')
    artigos = artigos.order_by(ordenar_por)

    # Paginação
    pagina = request.GET.get('pagina', 1)
    paginator = Paginator(artigos, 10)  # 10 artigos por página
    artigos_paginados = paginator.get_page(pagina)

    return render(request, 'lista_artigos.html', {
        'artigos': artigos_paginados,
        'filtros': filtros,
        'ordenar_por': ordenar_por
    })