from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^$',views.index, name='index'),
    url(r'^results/(?P<item_id>[0-9]+)/$', views.results, name='results'),
    url(r'^get_drugs/$', views.get_drugs, name='get_drugs'),
]
