#encoding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from TPVpnapp.views import *
#Estaticos y Media
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
#router.register

urlpatterns = [
    # Examples:
    # url(r'^$', 'TPVpn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'TPVpnapp.views.logAndReg'),
    url(r'^login/$', 'TPVpnapp.views.logAndReg'),
    url(r'^new_employer/$', 'TPVpnapp.views.neWorker'),
    url(r'^employers/$','TPVpnapp.views.listWorkers'),
    url(r'^employer_profile/(?P<pk>.*)/$', 'TPVpnapp.views.workerProfile'),
    url(r'^modWorker/(?P<pk>.*)/$', 'TPVpnapp.views.modWorker'),
    url(r'^index/$', 'TPVpnapp.views.index'),
    url(r'^initialData/$', 'TPVpnapp.views.initialData'),#AngularJS
    url(r'^addSell/$','TPVpnapp.views.addSell'),
    url(r'^logout/$', 'TPVpnapp.views.logoutSession'),
    url(r'^new_product/$', 'TPVpnapp.views.newProduct'),
    #url(r'^index/(?P<sale_id>[0-9]+)/$', 'TPVpnapp.views.actualSale'),
    #url(r'^deleteItem/(?P<sale_id>[0-9]+)/(?P<item_id>[0-9]+)/$', 'TPVpnapp.views.deleteItem'),
    #url(r'^deleteSale/(?P<sale_id>[0-9]+)/$', 'TPVpnapp.views.deleteSale'),
    url(r'^deleteClient/(?P<pk>.*)/$', 'TPVpnapp.views.deleteClient'),
    url(r'^products/$', 'TPVpnapp.views.listProducts'),
    url(r'^products/delete/(?P<product_id>[0-9]+)/$', 'TPVpnapp.views.deleteProduct'),
    url(r'^modProd/(?P<product_id>[0-9]+)/$', 'TPVpnapp.views.modifyProduct'),
    url(r'^new_client/$', 'TPVpnapp.views.newClient'),
    url(r'^clients/$', 'TPVpnapp.views.listClients'),
    url(r'^takeClients/$','TPVpnapp.views.takeClients'),#AngularJS
    url(r'^modCli/(?P<pk>.*)/$', 'TPVpnapp.views.modClient'),
    url(r'^client_profile/(?P<pk>.*)/$', 'TPVpnapp.views.clientProfile'),
    url(r'^cashFlows/$', 'TPVpnapp.views.cashFlows'),
    url(r'^takeSales/$', 'TPVpnapp.views.takeSales'),
    url(r'^sales/$', 'TPVpnapp.views.allSales'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
    ]
