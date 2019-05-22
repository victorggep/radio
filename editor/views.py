# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random
import string

import sendgrid
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import NoticiaForm, RegistrarUsuariForm, CanviContrasenyaForm, RecuperarContrasenyaForm, PerfilForm
from .models import Noticia, Perfil


def base_context(request):
    context = {
        'n_notificacions': 0,
        'peticions_de_registre': 0,
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
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = RegistrarUsuariForm()

    context['form'] = form
    return render(request, 'registration/registration.html', context)


def recuperar_contrasenya(request):
    context = {}
    if request.method == "POST":
        form = RecuperarContrasenyaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                random_string = ''.join(
                    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
                user = User.objects.get(email=email)
                user.set_password(random_string)
                sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
                data = {
                    "personalizations": [
                        {
                            "to": [
                                {
                                    "email": email
                                }
                            ],
                            "subject": "Nova contrasenya per Radio-Noticies"
                        }
                    ],
                    "from": {
                        "email": "noreply@radionoticies.com"
                    },
                    "content": [
                        {
                            "type": "text/plain",
                            "value": "La nova contrasenya és: {}".format(random_string)
                        }
                    ]
                }

                sg.client.mail.send.post(request_body=data)
                context['missatge'] = "S'ha enviat un mail amb la nova contrasenya"
            else:
                context['missatge'] = "No hi ha cap usuari amb aquest email"

    else:
        form = RecuperarContrasenyaForm()

    context['form'] = form
    return render(request, 'registration/recuperar_contrasenya.html', context)


@login_required(login_url=reverse_lazy('login'))
def canvi_contrasenya(request):
    context = {}
    if request.method == "POST":
        form = CanviContrasenyaForm(request.POST)
        if form.is_valid():
            username = request.user.username
            password = form.cleaned_data['password_antic']

            user = authenticate(username=username, password=password)
            if user is not None:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                context['form'] = form
                context['error'] = 'Contrasenya antiga incorrecta'
                return render(request, 'registration/canvi_contrasenya.html', context)
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
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": User.objects.get(username=username).email
                        }
                    ],
                    "subject": "Acces a Radio-Noticies"
                }
            ],
            "from": {
                "email": "noreply@radionoticies.com"
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": "L'administrador ja t'ha donat d'alta i pots accedir a la plataforma. Benvingut!"
                }
            ]
        }

        sg.client.mail.send.post(request_body=data)
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


@login_required(login_url=reverse_lazy('login'))
@staff_member_required(login_url=reverse_lazy('not_staff'))
def perfil(request, username):
    context = base_context(request)
    user = User.objects.get(username=username)
    noticies = Noticia.objects.filter(autor=user)
    pot_editar = username == request.user.username
    perfil, creat = Perfil.objects.get_or_create(user=request.user)
    context['user'] = user
    context['perfil'] = perfil
    context['noticies'] = noticies
    context['pot_editar'] = pot_editar
    return render(request, 'perfil/index.html', context)


@login_required(login_url=reverse_lazy('login'))
@staff_member_required(login_url=reverse_lazy('not_staff'))
def editar_perfil(request):
    context = base_context(request)
    if request.method == "POST":
        form = PerfilForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            cognom = form.cleaned_data['cognom']
            email = form.cleaned_data['email']
            telefon = form.cleaned_data['telefon']
            facebook = form.cleaned_data['facebook']
            linkedin = form.cleaned_data['linkedin']
            twitter = form.cleaned_data['twitter']
            User.objects.filter(username=request.user.username).update(email=email, first_name=nom, last_name=cognom)
            perfil = Perfil.objects.get(user=request.user)
            perfil.telefon = telefon
            perfil.facebook = facebook
            perfil.linkedin = linkedin
            perfil.twitter = twitter
            perfil.save()
            return HttpResponseRedirect(reverse_lazy('perfil', kwargs={'username': request.user.username}))
    else:
        form = PerfilForm()
        perfil = Perfil.objects.get(user=request.user)
        form.fields['nom'].initial = request.user.first_name
        form.fields['cognom'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email
        form.fields['telefon'].initial = perfil.telefon
        form.fields['facebook'].initial = perfil.facebook
        form.fields['linkedin'].initial = perfil.linkedin
        form.fields['twitter'].initial = perfil.twitter

    context['form'] = form
    return render(request, 'perfil/edit.html', context)


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
