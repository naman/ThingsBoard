from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.things),
    url(r'^things/(?P<thingid>\d+)/$', views.thing, name='thing'),
    url(r'^stats/$', views.Graph.as_view(), name='stats'),
    url(r'^addpermission/$', views.addpermission, name='addpermission'),
    url(r'^addtype/$', views.addtype, name='addtype'),
    url(r'^addroom/$', views.addroom, name='addroom'),
    url(r'^addowner/$', views.addowner, name='addowner'),
    url(r'^addurl/$', views.addurl, name='addurl'),
]
