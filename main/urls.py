from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^$',views.index, name='index'),
    url(r'^get_drugs/$', views.get_drugs, name='get_drugs'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^results/(?P<item_id>[0-9]+)/$', views.results, name='results'),
    url(r'^view_item/(?P<item_id>[0-9]+)/$', views.view_item, name='view_item'),
    url(r'^confirm/(?P<notification_id>[0-9]+)/$', views.confirm, name='confirm'),
    url(r'^confirm_delete/(?P<notification_id>[0-9]+)/$', views.confirm_delete, name='confirm_delete'),
    url(r'^respond_to_notification/(?P<notification_id>[0-9]+)/$', views.respond_to_notification, name='respond_to_notification'),
    url(r'^view_other_profile/(?P<user_id>[0-9]+)/$', views.view_other_profile, name='view_other_profile'),
    url(r'^make_transaction/(?P<notification_id>[0-9]+)/$', views.make_transaction, name='make_transaction'),

]
