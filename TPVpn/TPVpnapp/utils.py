#    -*- coding: UTF-8 -*-
#
#    --- License block --------------------------------------------------------
#    This file is part of TPVpn.
#
#    TPVpn is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TPVpn is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TPVpn.  If not, see <http://www.gnu.org/licenses/>.
#    --- End of License block -------------------------------------------------


import csv

from datetime import date

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from TPVpnapp.models import Client, Product, Worker, FullDirection, BankData


def update_offers(market):
    counter = False
    today = date.today()
    query = Product.objects.filter(market=market)
    for i in query:
        try:
            if i.offer:
                if i.offer.end_date < today:
                    i.offer.delete()
                    counter = True
        except:
            pass
    if counter:
        request = get_request()
        messages.success(request, "Ofertas actualizadas.<br>\
            Por favor, revise los productos")


def get_worker_market(request):
    try:
        worker = Worker.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(
            request,
            'El trabajador no está registrado en la plataforma.')

    return worker, worker.market


def get_categorys_subcategorys(products):
    categorys = set([])
    subcategorys = set([])
    [[categorys.add(i.category), subcategorys.add(i.subcategory)]
        for i in products]
    if categorys:
        categorys = sorted(categorys, key=unicode.lower)
    if subcategorys:
        subcategorys = sorted(subcategorys, key=unicode.lower)
    return categorys, subcategorys


def search_clients(request, search_clie, market_now, clients):
    aux = search_clie['array'].value()
    if aux != '':
        cad = aux.split(' ')
        list_aux = set([])
        for word in cad:
            aux_n = Client.objects.filter(name__icontains=word,
                                          market=market_now)
            aux_d = Client.objects.filter(dni__icontains=word,
                                          market=market_now)
            aux_e = Client.objects.filter(market=market_now,
                                          email__icontains=word
                                          )
            [list_aux.add(i.dni) for i in (aux_n | aux_d | aux_e)]
        if not list_aux:
            messages.error(request,
                           ('No se han encontrado clientes ' +
                            'con los datos especificados.'))
        else:
            clients = Client.objects.filter(dni__in=list_aux)
    return clients


def search_workers(request, workers, market_now):
    aux = request.POST.get('array', False)
    cad = aux.split(' ')
    aux_c = []
    for word in cad:
        aux_n_dictionary = {'user__first_name__icontains':
                            word,
                            'market': market_now}
        aux_n = Worker.objects.filter(**aux_n_dictionary)
        aux_a_dictionary = {'user__last_name__icontains': word,
                            'market': market_now}
        aux_a = Worker.objects.filter(**aux_a_dictionary)
        aux_l_dictionary = {'user__username__icontains': word,
                            'market': market_now}
        aux_l = Worker.objects.filter(**aux_l_dictionary)
        aux_d = Worker.objects.filter(dni__icontains=word,
                                      market=market_now)
        if aux_n or aux_a or aux_l or aux_d:
            for i in (list(aux_n) + list(aux_a) + list(aux_l) +
                      list(aux_d)):
                counter = 0
                for j in aux_c:
                    if i == j:
                        counter = 1
                if counter == 0:
                    if i:
                        aux_c.append(i)
    if aux_c:
        workers = aux_c
    else:
        messages.warning(request, 'No se han encontrado trabajadores.')

    return workers


def paginator_function(request, query):
    paginator = Paginator(query, 4)
    page = request.GET.get('page', 1)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(page)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)

    return query, page


def get_ivas(sales_query):
    iva21 = 0
    iva10 = 0
    iva4 = 0
    for sale in sales_query:
        for prod in sale.productsale_set.filter(product__iva=21):
            iva21 += float("{0:.2f}".format(prod.totAmount * 0.21))
        for prod in sale.productsale_set.filter(product__iva=10):
            iva10 += float("{0:.2f}".format(prod.totAmount * 0.1))
        for prod in sale.productsale_set.filter(product__iva=4):
            iva4 += float("{0:.2f}".format(prod.totAmount * 0.04))

    return iva21, iva10, iva4


def get_total_invoice(sales_query):
    coste, ingreso, beneficio = 0, 0, 0

    for sale in sales_query:
        for prod in sale.productsale_set.filter(product__isnull=False):
            coste += float("{0:.2f}".format(
                prod.product.buyPrice * prod.amount))
            ingreso += float("{0:.2f}".format(
                prod.product.sellPrice * prod.amount))

    beneficio = float("{0:.2f}".format(ingreso - coste))

    return coste, ingreso, beneficio


def get_method_freq(market_now):
    methods = set([])
    freq = set([])
    query = Client.objects.filter(market=market_now)
    [(freq.add(i.bank.frequency), methods.add(i.bank.payment_method))
        for i in query if i.bank]
    return methods, freq

CLIENT_MAP = {
    'nombre': 'name',
    'apellidos': 'surname',
    'nif': 'dni',
    'email': 'email',
    'telfijo': 'tel',
    'telmovil': 'tel2',
    'fecha_alta': 'date',
    'fecha_baja': 'expire_date',
    'saldo': 'wallet',
}


DIRECTION_MAP = {
    'domicilio': 'direction',
    'cp': 'postalCode',
    'localidad': 'location',
    'provincia': 'province',
}

BANK_MAP = {
    'modopago': 'payment_method',
    'nombretitularcuenta': 'owner_name',
    'apellidostitularcuenta': 'owner_surname',
    'niftitularcuenta': 'owner_nif',
    'banco': 'bank_name',
    'ncuenta': 'account_number',
    'cuota': 'subscription',
    'frecpago': 'frequency',
    'observaciones': 'observations',
}


def import_csv(market, file):
    content = csv.reader(file)
    content = [row for row in content]
    keys = content[0]

    del content[0]

    all_dict = []

    for values in content:
        aux_dict = {}
        for key, value in zip(keys, values):
            aux_dict.update({key: value})
        all_dict.append(aux_dict)

    save_data(market, all_dict)
    return True


def save_data(market, all_dict):
    for i in all_dict:
        direction = {}
        bank = {}
        client = {}
        for key, value in DIRECTION_MAP.items():
            direction.update({
                value: i[key]
            })
        direction_instance = FullDirection.objects.create(**direction)

        for key, value in BANK_MAP.items():
            bank.update({
                value: i[key]
            })
        bank_instance = BankData.objects.create(**bank)

        for key, value in CLIENT_MAP.items():
            client.update({
                value: i[key]
            })
        try:
            dni = client['dni']
            if '-' in dni:
                dni = dni.replace('-', '')
                client['dni'] = dni
            client_instance = Client.objects.get(market=market,
                                                 dni=client['dni'])
            # client_instance.update(**client)
            for key, value in client.items():
                setattr(client_instance, key, value)
        except ObjectDoesNotExist:
            client_instance = Client.objects.create(market=market, **client)

        client_instance.home = direction_instance
        client_instance.bank = bank_instance
        client_instance.save()


try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()


class ThreadLocalMiddleware(object):
    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response


def get_request():
    return getattr(_thread_locals, 'request', None)
