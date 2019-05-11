# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

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
    context = {}
    return render(request, 'index/index.html', context)
