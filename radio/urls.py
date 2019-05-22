"""radio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from editor import views as edit_views
from django.urls import reverse_lazy

urlpatterns = [
    # Editor
    url(r'^', include('editor.urls')),
    # Admin
    url(r'^admin/', admin.site.urls),
    # Gestio usuaris
    url(r'^register$', edit_views.registration, name='registration'),
    url(r'^usuaris/recuperar_contrasenya$', edit_views.recuperar_contrasenya, name='recuperar_contrasenya'),
    url(r'^usuaris/canvi_contrasenya$', edit_views.canvi_contrasenya, name='canvi_contrasenya'),
    url(r'^usuaris/gestio$', edit_views.gestio_usuaris, name='gestio_usuaris'),
    url(r'^usuaris/gestio/(?P<username>[\w\-.]+)/confirmar$', edit_views.confirmar_usuari, name='confirmar_usuari'),
    url(r'^usuaris/gestio/(?P<username>[\w\-.]+)/denegar$', edit_views.denegar_usuari, name='denegar_usuari'),
    url(r'^usuaris/gestio/(?P<username>[\w\-.]+)/treure_admin$', edit_views.treure_administrador, name='treure_administrador'),
    url(r'^usuaris/gestio/(?P<username>[\w\-.]+)/fer_admin$', edit_views.fer_administrador, name='fer_administrador'),
    url(r'^usuaris/gestio/(?P<username>[\w\-.]+)/esborrar$', edit_views.esborrar_usuari, name='esborrar_usuari'),
    # Errors
    url(r'^not-staff$', edit_views.not_staff, name='not_staff'),
    url(r'^sense_permis$', edit_views.sense_permis, name='sense_permis'),
    # Login
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': reverse_lazy('index')}, name='logout'),
] + static(settings.STATIC_URL)
