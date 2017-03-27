from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^things/$', views.things),
    url(r'^things/(?P<thingid>\d+)/$', views.thing),
    # url(r'^things/)
]
