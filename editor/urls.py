from django.conf.urls import url
from editor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil/editar$', views.editar_perfil, name='editar_perfil'),
    url(r'^perfil/(?P<username>[\w\-.]+)$', views.perfil, name='perfil'),
    url(r'^noticies/(?P<id>[0-9]+)$', views.veure_noticia, name='veure_noticia'),
    url(r'^noticies/filtrar$', views.filtrar_noticies, name='filtrar_noticies'),
    url(r'^noticies/crear$', views.crear_noticia, name='crear_noticia')
]
