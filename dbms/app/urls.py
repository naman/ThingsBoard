from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index),
	url(r'^customer/$', views.newcustomer),
	url(r'^customer/(?P<cid>\d+)/$', views.customer_edit),
	url(r'^customer/(?P<cid>\d+)/delete/$', views.customer_delete),
	url(r'^employee/$', views.newemployee),
	url(r'^employee/(?P<eid>\d+)/$', views.employee_edit),
	url(r'^employee/(?P<eid>\d+)/delete/$', views.employee_delete),
	url(r'^order/$', views.neworder),
	url(r'^order/(?P<oid>\d+)/$', views.order_edit),
	url(r'^order/(?P<oid>\d+)/delete/$', views.order_delete),
	url(r'^part/$', views.newpart),
	url(r'^part/(?P<pid>\d+)/$', views.part_edit),
	url(r'^part/(?P<pid>\d+)/delete/$', views.part_delete),
	url(r'^orderpart/$', views.order_per_part),
	url(r'^orderpart/(?P<opid>\d+)/$', views.order_per_part_update),
	url(r'^orderpart/(?P<opid>\d+)/delete/$', views.order_per_part_delete),
	url(r'^query/$', views.query ),
	
]