from django.conf.urls import url
from editor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^noticies/crear$', views.crear_noticia, name='crear_noticia'),
]
