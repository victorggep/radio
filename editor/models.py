# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Noticia(models.Model):
    titular = models.CharField(max_length=500)
    resum = models.TextField()
    cos_noticia = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
