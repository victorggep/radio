# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Perfil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, null=True)
    facebook = models.CharField(max_length=100, null=True)
    linkedin = models.CharField(max_length=100, null=True)
    twitter = models.CharField(max_length=100, null=True)


class Noticia(models.Model):
    SECCIONS = (
        ('L', 'Local'),
        ('I', 'Internacional'),
        ('P', 'Política'),
        ('E', 'Economia'),
        ('S', 'Esports'),
        ('O', 'Opinió'),
        ('A', 'Altres'),

    )
    seccio = models.CharField(max_length=1, choices=SECCIONS, default='A')
    titular = models.CharField(max_length=500)
    cos_noticia = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
