from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    # Rotas do frontend
    path('criar/', views.criar, name='criar'),  
    path('lista_artigos/', views.lista_artigos, name='lista_artigos'),
    path('artigos/<int:artigo_id>/editar/', views.editar, name='editar'),
    path('detalhes/<int:artigo_id>/', views.detalhes_artigo, name='detalhes_artigo'),
    path('download_artigo/<int:artigo_id>/', views.download_artigo, name='download_artigo'),
    path('excluir_artigo/<int:artigo_id>/', views.excluir_artigo, name='excluir_artigo'),
    path('busca/', views.busca_artigos, name='busca_artigos'),
]
