# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import NoticiaForm
from .models import Noticia

# Create your views here.


################################
#######      Index      ########
################################

@login_required(login_url=reverse_lazy('login'))
def index(request):
    """
    centers = Centers.objects.filter(users__username__contains=request.user.username)
    roads = Roads.objects.filter(center__users__username__contains=request.user.username)
    context = {}
    context['centers'] = centers
    context['roads'] = roads
    """
    noticies = Noticia.objects.all()
    context = {
        'noticies': noticies
    }
    return render(request, 'index/index.html', context)



@login_required(login_url=reverse_lazy('login'))
def crear_noticia(request):
    context = {}
    if request.method == "POST":
        form = NoticiaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = NoticiaForm()

    context['form'] = form
    return render(request, 'noticies/crear.html', context)
