from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.things),
    url(r'^things/(?P<thingid>\d+)/$', views.thing, name='thing'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^addurl/$', views.addurl, name='addurl'),
    url(r'^addpermission/$', views.addpermission, name='addpermission'),
    url(r'^addtype/$', views.addtype, name='addtype'),
    url(r'^addroom/$', views.addroom, name='addroom'),
]
