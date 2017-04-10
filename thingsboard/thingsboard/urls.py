from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('', url('', include('app.urls'))) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
