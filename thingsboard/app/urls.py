from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^things/$', views.things),
    url(r'^detect/$', views.detect),
    url(r'^owner/$', views.owner)
]
