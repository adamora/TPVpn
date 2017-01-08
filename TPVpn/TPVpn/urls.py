# encoding:utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

# from TPVpnapp.views import (addSell, index, initialData, listWorkers,
#                             logAndReg, logoutSession, modWorker, neWorker,
#                             workerProfile, )

from rest_framework import routers

router = routers.DefaultRouter()
# router.register

urlpatterns = [
    # Examples:
    # url(r'^$', 'TPVpn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'TPVpnapp.views.log_and_reg'),
    url(r'^login/$', 'TPVpnapp.views.log_and_reg'),
    url(r'^new_employer/$', 'TPVpnapp.views.new_worker'),
    url(r'^employers/$', 'TPVpnapp.views.list_workers'),
    url(r'^employer_profile/(?P<pk>.*)/$', 'TPVpnapp.views.worker_profile'),
    url(r'^modWorker/(?P<pk>.*)/$', 'TPVpnapp.views.mod_worker'),
    url(r'^index/$', 'TPVpnapp.views.index'),
    url(r'^initial_data/$', 'TPVpnapp.views.initial_data'),
    url(r'^addSell/$', 'TPVpnapp.views.add_sell'),
    url(r'^logout/$', 'TPVpnapp.views.logout_session'),
    url(r'^new_product/$', 'TPVpnapp.views.new_product'),
    # url(r'^index/(?P<sale_id>[0-9]+)/$', 'TPVpnapp.views.actualSale'),
    # url(r'^deleteItem/(?P<sale_id>[0-9]+)/(?P<item_id>[0-9]+)/$',
    #     'TPVpnapp.views.deleteItem'),
    # url(r'^deleteSale/(?P<sale_id>[0-9]+)/$', 'TPVpnapp.views.deleteSale'),
    url(r'^deleteClient/(?P<pk>.*)/$', 'TPVpnapp.views.delete_client'),
    url(r'^products/$', 'TPVpnapp.views.list_products'),
    url(r'^products/delete/(?P<product_id>[0-9]+)/$',
        'TPVpnapp.views.delete_product'),
    url(r'^modProd/(?P<product_id>[0-9]+)/$', 'TPVpnapp.views.modify_product'),
    url(r'^new_client/$', 'TPVpnapp.views.new_client'),
    url(r'^clients/$', 'TPVpnapp.views.list_clients'),
    url(r'^take_clients/$', 'TPVpnapp.views.take_clients'),
    url(r'^modCli/(?P<pk>.*)/$', 'TPVpnapp.views.mod_client'),
    url(r'^client_profile/(?P<pk>.*)/$', 'TPVpnapp.views.client_profile'),
    url(r'^cashFlows/$', 'TPVpnapp.views.cash_flows'),
    url(r'^takeSales/$', 'TPVpnapp.views.take_sales'),
    url(r'^sales/$', 'TPVpnapp.views.all_sales'),
    url(r'^configuration/$', 'TPVpnapp.views.configuration'),
    url(r'^offer/delete/(?P<product_id>[0-9]+)/$',
        'TPVpnapp.views.delete_offer'),
    # url(r'^invoice-report/$', 'TPVpnapp.views.invoice_report'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root':
                                             settings.MEDIA_ROOT, }),
    ]
