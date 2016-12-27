from django.conf.urls import include, url
from django.contrib import admin
from app import urls


urlpatterns = [
    # Examples:
    # url(r'^$', 'dbms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
