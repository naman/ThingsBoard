from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.things),
    url(r'^things/(?P<thingid>\d+)/$', views.thing, name='thing')
]
