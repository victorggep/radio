# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import NoticiaForm, RegistrarUsuariForm, CanviContrasenyaForm
from .models import Noticia
import os
import sendgrid
from sendgrid.helpers.mail import *


def base_context(request):
    context = {
        'n_notificacions': 0,
        'peticions_de_registre': 0
    }
    if request.user.is_superuser:
        peticions_registre = User.objects.filter(is_staff=False).count()
        if peticions_registre > 0:
            context['n_notificacions'] += peticions_registre
            context['peticions_de_registre'] = peticions_registre
    return context

################################
#            Usuaris           #
################################


def registration(request):
    context = {}
    if request.method == "POST":
        form = RegistrarUsuariForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = RegistrarUsuariForm()

    context['form'] = form
    return render(request, 'registration/registration.html', context)


@login_required(login_url=reverse_lazy('login'))
def canvi_contrasenya(request):
    context = {}
    if request.method == "POST":
        form = CanviContrasenyaForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = CanviContrasenyaForm()

    context['form'] = form
    return render(request, 'registration/canvi_contrasenya.html', context)


@login_required(login_url=reverse_lazy('login'))
def gestio_usuaris(request):
    if request.user.is_superuser:
        context = base_context(request)
        users = User.objects.all()
        context['users'] = users
        return render(request, 'registration/gestio_usuaris.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('sense_permis'))


@login_required(login_url=reverse_lazy('login'))
def confirmar_usuari(request, username):
    if request.user.is_superuser:
        User.objects.filter(username=username).update(is_staff=True)
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = "noreply@radio-noticies.com"
        subject = "Radio-Noticies Login"
        to_emails = User.objects.get(username=username).email.encode('utf-8')
        content = Content("text/plain", "L'administrador ja t'ha donat d'alta i pots accedir a la plataforma. Benvingut!")
        mail = Mail(from_email=from_email, to_emails=to_emails, subject=subject, plain_text_content=content)
        sg.client.mail.send.post(request_body=mail.get())
        context = base_context(request)
        users = User.objects.all()
        context['users'] = users
        return render(request, 'registration/gestio_usuaris.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('sense_permis'))


@login_required(login_url=reverse_lazy('login'))
def denegar_usuari(request, username):
    if request.user.is_superuser:
        User.objects.filter(username=username).delete()
        context = base_context(request)
        users = User.objects.all()
        context['users'] = users
        return render(request, 'registration/gestio_usuaris.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('sense_permis'))


@login_required(login_url=reverse_lazy('login'))
def treure_administrador(request, username):
    if request.user.is_superuser:
        User.objects.filter(username=username).update(is_superuser=False)
        context = base_context(request)
        users = User.objects.all()
        context['users'] = users
        return render(request, 'registration/gestio_usuaris.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('sense_permis'))


@login_required(login_url=reverse_lazy('login'))
def fer_administrador(request, username):
    if request.user.is_superuser:
        User.objects.filter(username=username).update(is_superuser=True)
        context = base_context(request)
        users = User.objects.all()
        context['users'] = users
        return render(request, 'registration/gestio_usuaris.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('sense_permis'))


@login_required(login_url=reverse_lazy('login'))
def esborrar_usuari(request, username):
    if request.user.is_superuser:
        User.objects.filter(username=username).delete()
        context = base_context(request)
        users = User.objects.all()
        context['users'] = users
        return render(request, 'registration/gestio_usuaris.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('sense_permis'))


@login_required(login_url=reverse_lazy('login'))
def not_staff(request):
    context = {}
    return render(request, 'error/not_staff.html', context)


@login_required(login_url=reverse_lazy('login'))
def sense_permis(request):
    context = {}
    return render(request, 'error/sense_permis.html', context)


################################
#            Index             #
################################

@login_required(login_url=reverse_lazy('login'))
@staff_member_required(login_url=reverse_lazy('not_staff'))
def index(request):
    context = base_context(request)
    noticies = Noticia.objects.all()
    context['noticies'] = noticies
    return render(request, 'index/index.html', context)


################################
#           Noticies           #
################################
@login_required(login_url=reverse_lazy('login'))
@staff_member_required(login_url=reverse_lazy('not_staff'))
def crear_noticia(request):
    context = base_context(request)
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
