from django.db import models
import os

# Create your models here.
class Artigo(models.Model):
    titulo = models.CharField(max_length=255)
    autores = models.CharField(max_length=255)
    resumo = models.CharField(max_length=255)
    abstract = models.TextField()
    palavras_chave = models.TextField()
    data = models.DateField(blank=True, null=True)
    revista = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='arquivos/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
