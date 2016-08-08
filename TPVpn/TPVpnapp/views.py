# encoding:utf-8
import copy
from datetime import date, datetime

from TPVpnapp.forms import (ClientForm, FullDirectionForm, InputMoney,
                            LoginForm, NotificationForm, PasswordMarketForm,
                            ProductForm, ProviderForm,
                            RegisterBusinessForm, RegisterWorker,
                            SearchClientForm, SearchProduct,
                            SearchWorkerForm, StockForm, UserForm)
from TPVpnapp.models import (Client, Market, Notification, Product,
                             ProductSale, Provider, Sale, Worker)
from TPVpnapp.serializers import (ClientSerializer, ProductSerializer,
                                  SaleSerializer)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """An HttpResponse that renders its content into JSON."""

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def log_and_reg(request):
    if not request.user.is_anonymous():
        return redirect('/index')
    if request.method == 'POST':
        loginuser = LoginForm(data=request.POST)
        # newuser = UserForm(request.POST)
        # neworker = RegisterWorker(request.POST)
        newbusiness = RegisterBusinessForm(request.POST)
        new_address = FullDirectionForm(request.POST)

        if request.POST['inputInLogin'] == 'loginUser':
            if loginuser.is_valid():
                user = request.POST.get('username', False)
                key = request.POST.get('password', False)
                return new_login(request, user, key)
            else:
                print "¡FALLO EN LA OBTENCIÓN DEL LOGIN!"
        if request.POST['inputInLogin'] == 'registerMarket':
            if new_address.is_valid():
                addr = new_address.save()
            else:
                print "NO SE HA PODIDO GUARDAR DIRECCION"
            if newbusiness.is_valid():
                if (request.POST.get('secretKey', True) ==
                        request.POST.get('secretKey2', True)):
                    business = newbusiness.save(commit=False)
                    business.direction = addr
                    business.save()
                    return redirect('/login')
                else:
                    return "NO SE HA PODIDO CREAR MERCADO"
    else:
        # newuser = UserForm()
        # neworker = RegisterWorker()
        loginuser = LoginForm()
        new_address = FullDirectionForm()
        newbusiness = RegisterBusinessForm()
    return render(request, 'login.html', {'loginuser': loginuser,
                                          'newAddress': new_address,
                                          'newbusiness': newbusiness})


@login_required(login_url='/')
def new_worker(request):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    market_now = worker_now.market
    if request.method == 'POST':
        newuser = UserForm(request.POST)
        neworker = RegisterWorker(request.POST, request.FILES)
        new_address = FullDirectionForm(request.POST)
        password = PasswordMarketForm(request.POST)
        if request.POST['neWorkerForm'] == 'registerUser':
            if (newuser.is_valid() * new_address.is_valid() *
                    neworker.is_valid() * password.is_valid()):
                if (request.POST.get('secretKey', False) ==
                        market_now.secretKey):
                    user_aux = newuser.save()
                    ''' >>>>> FUNCIONA PARO NO UTIL -> NO LOGIN
                    user = request.POST.get('username',False)
                    key = request.POST.get('password1',False)
                    '''
                    addr = new_address.save()
                    worker_aux = neworker.save(commit=False)
                    worker_aux.user = user_aux
                    worker_aux.market = market_now
                    worker_aux.home = addr
                    worker_aux.save()
                    return redirect('/employers')
                else:
                    password['secretKey'].error = "¡Contraseña incorrecta!"
            elif not newuser.is_valid():
                print "NO SE HA CREADO BIEN EL USER"
            elif not new_address.is_valid():
                print "NO SE HA CREADO BIEN LA DIRECCIÓN"
            elif not neworker.is_valid():
                print "NO SE HA CREADO BIEN EL USUARIO"
            else:
                print "¡ERROR! CONTACTE CON EL SERVICIO TÉCNICO"
                return render(request, 'page_404.html')

    else:
        newuser = UserForm()
        neworker = RegisterWorker()
        new_address = FullDirectionForm()
        password = PasswordMarketForm()
    return render(request, 'workerForm.html', {'newuser': newuser,
                                               'neworker': neworker,
                                               'newAddress': new_address,
                                               'worker_now': worker_now,
                                               'password': password})


@login_required(login_url='/')
def list_workers(request):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    market_now = worker_now.market

    fail = None
    workers = Worker.objects.filter(market=market_now)

    if request.method == 'POST':
        search = SearchWorkerForm(request.POST)
        notification = NotificationForm(request.POST)
        if 'searchWorkerForm' in request.POST:
            if request.POST['searchWorkerForm'] == 'searchWorker':
                if search.is_valid():
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
                        fail = "title: 'Error', type: 'error', text: 'No se  \
                                han encontrado trabajadores.'"
        if 'newNotification' in request.POST:
            for i in workers:
                if request.POST['newNotification'] == i.dni:
                    if notification.is_valid():
                        aux = notification.save(commit=False)
                        aux.reciver = i
                        aux.writer = worker_now
                        aux.typeNote = 'normal'
                        aux.save()
                        notification = NotificationForm()
    else:
        search = SearchWorkerForm()
        notification = NotificationForm()

    to_return = {'worker_now': worker_now, 'workers': workers,
                 'search': search, 'notification': notification, 'fail': fail}

    return render(request, 'employers.html', to_return)


@login_required(login_url='/')
def mod_worker(request, pk):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    market_now = worker_now.market
    fail = None

    worker_profile = Worker.objects.get(dni=pk)

    if worker_profile == worker_now:
        if request.method == 'POST':
            newuser = UserForm(request.POST, instance=worker_profile.user)
            neworker = RegisterWorker(request.POST, instance=worker_profile)
            new_address = FullDirectionForm(request.POST,
                                            instance=worker_profile.home)
            password = PasswordMarketForm(request.POST)
            if request.POST['neWorkerForm'] == 'registerUser':
                if (newuser.is_valid() * new_address.is_valid() *
                        neworker.is_valid() * password.is_valid()):
                    if (request.POST.get('secretKey', False) ==
                            market_now.secretKey):
                        user_aux = newuser.save()
                        addr = new_address.save()
                        worker_aux = neworker.save(commit=False)
                        if not request.POST.get('genre', False):
                            worker_aux.genre = worker_profile.genre
                        worker_aux.user = user_aux
                        worker_aux.market = market_now
                        worker_aux.home = addr
                        worker_aux.save()
                        return new_login(request, worker_aux.user.username,
                                         request.POST.get('password1', False))
                    else:
                        password['secretKey'].error = "¡Contraseña incorrecta!"

        else:
            newuser = UserForm(instance=worker_profile.user)
            neworker = RegisterWorker(instance=worker_profile)
            new_address = FullDirectionForm(instance=worker_profile.home)
            password = PasswordMarketForm()

        to_return = {'worker_now': worker_now, 'fail': fail,
                     'neworker': neworker, 'newAddress': new_address,
                     'password': password, 'newuser': newuser}
    else:
        return redirect('/employers')

    return render(request, 'workerForm.html', to_return)


@login_required(login_url='/')
def worker_profile(request, pk):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    fail = None

    worker_profile = Worker.objects.get(dni=pk)
    notifications = Notification.objects.filter(reciver=worker_profile)

    to_return = {'worker_now': worker_now, 'workerProfile': worker_profile,
                 'notifications': notifications, 'fail': fail}

    return render(request, 'employerProfile.html', to_return)


def new_login(request, user, key):
    print "El usuario ", user, " intenta iniciar sesión."
    access = authenticate(username=user, password=key)
    if access is not None:
        print 'Autenticado'
        if access.is_active:
            login(request, access)
            return redirect('/index')
        else:
            return False
    else:
        return False


@login_required(login_url='/')
def logout_session(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def new_product(request):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    if request.method == 'POST':
        newprovider = ProviderForm(request.POST)
        newprod = ProductForm(request.POST, request.FILES)
        if request.POST['inputInNewProd'] == 'newProvider':
            if newprovider.is_valid():
                if not Provider.objects.filter(
                    namePro=newprovider['namePro'].value(),
                    market=worker_now.market
                ):
                    provider = newprovider.save(commit=False)
                    provider.market = worker_now.market
                    provider.save()
                else:
                    provider = Provider.objects.get(
                        namePro=newprovider['namePro'].value(),
                        market=worker_now.market
                    )
                newprod = ProductForm(initial={'provider': provider})
                newprovider = ProviderForm(instance=provider)
        elif request.POST['inputInNewProd'] == 'newProd':
            if newprod.is_valid():
                prod = newprod.save(commit=False)
                prod.market = worker_now.market
                prod.offer = prod.sellPrice
                if not prod.barCode:
                    prod.barCode = 'Vacio'
                if newprod['image'].value():
                    newprod['image'].error = 'Vuelva a seleccionar la imagen.'
                if prod.buyPrice > prod.sellPrice:
                    newprod['sellPrice'].error = "¡El precio de venta no puede \
                                                  ser superior al de compra!"
                elif prod.amount < 0:
                    newprod['amount'].error = '¡La cantidad de producto debe \
                                               ser mayor a 0!'
                else:
                    prod.save()
                    return redirect('/new_product')
            else:
                print "¡Error!: No se han cumplimentado correctamente los \
                       datos del producto."
    else:
        newprovider = ProviderForm()
        newprod = ProductForm()

    to_return = {'worker_now': worker_now, 'newprovider': newprovider,
                 'newprod': newprod}

    return render(request, 'productForm.html', to_return)


@login_required(login_url='/')
def list_products(request):
    worker_now = Worker.objects.get(user=request.user)
    market_now = worker_now.market
    products = Product.objects.filter(market=market_now)
    fail = None

    if request.method == 'POST':
        search_product = SearchProduct(request.POST)
        mod_quantity = StockForm(request.POST)
        if 'searching' in request.POST:
            if request.POST['searching'] == 'searchProd':
                if search_product.is_valid():
                    aux = search_product['search'].value()
                    if aux != '':
                        cad = aux.split(' ')
                        aux_cad = []
                        for word in cad:
                            aux_n = Product.objects.filter(
                                market=market_now,
                                name__icontains=word)
                            aux_b = Product.objects.filter(
                                brand__icontains=word, market=market_now)
                            aux_p = Product.objects.filter(
                                market=market_now,
                                provider__namePro__icontains=word)
                            aux_c = Product.objects.filter(
                                category__icontains=word, market=market_now)
                            aux_sc = Product.objects.filter(
                                subcategory__icontains=word, market=market_now)
                            aux_bc = Product.objects.filter(
                                barCode__icontains=word, market=market_now)
                            if (aux_n or aux_b or aux_p or aux_c or aux_sc or
                                    aux_bc):
                                for i in (list(aux_n) + list(aux_b) +
                                          list(aux_p) + list(aux_c) +
                                          list(aux_sc) + list(aux_bc)):
                                    counter = 0
                                    for j in aux_cad:
                                        if i == j:
                                            counter = 1
                                    if counter == 0:
                                        if i:
                                            aux_cad.append(i)
                        if not aux_cad:
                            fail = "title: 'Error', type: 'error', text: 'No \
                                    se han encontrado productos.'"
                        else:
                            products = aux_cad
        if 'newQuantity' in request.POST:
            for i in products:
                if request.POST['newQuantity'] == str(i.pk):
                    if mod_quantity.is_valid():
                        if (mod_quantity['new'].value() and
                                mod_quantity['add'].value()):
                            mod_quantity['new'].error = '¡Error! Ambos campos \
                                                        no pueden ser \
                                                        cumplimentados.'
                            fail = "title: 'Error', type: 'error', text: \
                                    'Ambos campos de stock en \
                                    <big><b>" + i.name + "</b></big> \
                                    no pueden ser cumplimentados.'"
                        elif mod_quantity['new'].value() != '':
                            if float(mod_quantity['new'].value()) < 0:
                                mod_quantity['new'].error = '¡Error! El valor \
                                                            debe ser mayor o \
                                                            igual a cero.'
                                fail = "title: 'Error', type: 'error', \
                                        text: 'El valor introducido en \
                                        <big><b>" + i.name + "</b></big> debe \
                                        ser mayor o igual a cero.'"
                            else:
                                i.amount = mod_quantity['new'].value()
                                i.save()
                        elif mod_quantity['add'].value() != '':
                            i.amount += float(mod_quantity['add'].value())
                            i.save()
                        else:
                            mod_quantity['new'].error = '¡Error! Uno de los \
                                                        campos debe ser \
                                                        cumplimentado.'
                            fail = "title: 'Aviso', type: 'warning', \
                                    text: 'Uno de los campos de stock en \
                                    <big><b>" + i.name + "</b></big> \
                                    debe ser cumplimentado.'"

    else:
        search_product = SearchProduct()
        mod_quantity = StockForm()

    to_return = {'worker_now': worker_now, 'market_now': market_now,
                 'products': products, 'search_product': search_product,
                 'mod_quantity': mod_quantity, 'fail': fail}

    return render(request, 'products.html', to_return)


@login_required(login_url='/')
def delete_product(request, product_id):
    worker_now = Worker.objects.get(user=request.user)
    market_now = worker_now.market
    product = Product.objects.get(id=product_id, market=market_now)

    if product:
        product.delete()
    # else:
        # AGREGAR UNA NOTIFICACION AL USUARIO
    return redirect('/products')


@login_required(login_url='/')
def modify_product(request, product_id):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    product = Product.objects.get(id=product_id, market=worker_now.market)
    if request.method == 'POST':
        newprovider = ProviderForm(request.POST)
        newprod = ProductForm(request.POST, request.FILES, instance=product)
        if request.POST['inputInNewProd'] == 'newProvider':
            if newprovider.is_valid():
                provider = newprovider.save(commit=False)
                provider.market = worker_now.market
                provider.save()
                product.provider = provider
                product.save()
                return redirect('/modProd/' + product_id)
        if request.POST['inputInNewProd'] == 'newProd':
            if newprod.is_valid():
                prod = newprod.save(commit=False)
                prod.offer = prod.sellPrice
                if not prod.barCode:
                    prod.barCode = 'Vacio'
                if prod.buyPrice > prod.sellPrice:
                    newprod['sellPrice'].error = '¡El precio de venta no \
                                                  puede ser superior al de \
                                                  compra!'
                elif prod.amount < 0:
                    newprod['amount'].error = '¡La cantidad de producto debe \
                                               ser mayor a 0!'
                else:
                    prod.save()
                    return redirect('/products')
            else:
                print "¡Error!: No se han cumplimentado correctamente los \
                       datos del producto."
    else:
        newprovider = ProviderForm()
        newprod = ProductForm(instance=product)
    return render(request, 'productForm.html',
                  {'worker_now': worker_now, 'newprovider': newprovider,
                   'newprod': newprod},
                  context_instance=RequestContext(request))


@login_required(login_url='/')
def new_client(request):
    worker_now = Worker.objects.get(user=request.user)

    if request.method == 'POST':
        new_client = ClientForm(request.POST, request.FILES)
        if request.POST['inputInNewCli'] == 'newCli':
            if new_client.is_valid():
                aux_cli = new_client.save(commit=False)
                aux_cli.market = worker_now.market
                if not aux_cli.email:
                    aux_cli.email = None
                aux_cli.save()
                return redirect('/clients')
    else:
        new_client = ClientForm()

    to_return = {'new_client': new_client, 'worker_now': worker_now}

    return render(request, 'new_client.html', to_return)


@login_required(login_url='/')
def list_clients(request):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    market_now = worker_now.market
    clients = Client.objects.filter(market=market_now)
    fail = None

    if request.method == 'POST':
        search_clie = SearchClientForm(request.POST)
        notification = NotificationForm(request.POST)
        wallet = InputMoney(request.POST)
        if 'searchCli' in request.POST:
            if request.POST['searchCli'] == 'newSearch':
                if search_clie.is_valid():
                    aux = search_clie['array'].value()
                    if aux != '':
                        cad = aux.split(' ')
                        list_aux = []
                        for word in cad:
                            aux_n = Client.objects.filter(name__icontains=word,
                                                          market=market_now)
                            aux_d = Client.objects.filter(dni__icontains=word,
                                                          market=market_now)
                            aux_e = Client.objects.filter(market=market_now,
                                                          email__icontains=word
                                                          )
                            if aux_n or aux_d or aux_e:
                                for i in (list(aux_n) + list(aux_d) +
                                          list(aux_e)):
                                    counter = 0
                                    for j in list_aux:
                                        if i == j:
                                            counter = 1
                                    if counter == 0:
                                        if i:
                                            list_aux.append(i)
                        if not list_aux:
                            fail = "title: 'Error', type: 'error', text: 'No \
                                    se han encontrado clientes.'"
                        else:
                            clients = list_aux
        if 'newNotification' in request.POST:
            for i in clients:
                if request.POST['newNotification'] == i.pk:
                    if notification.is_valid():
                        note_aux = notification.save(commit=False)
                        note_aux.writer = worker_now
                        note_aux.reciverCli = i
                        note_aux.typeNote = 'normal'
                        note_aux.save()
                        notification = NotificationForm()
        if 'modWallet' in request.POST:
            for i in clients:
                if request.POST['modWallet'] == i.pk:
                    if wallet.is_valid():
                        new = wallet['new'].value()
                        add = wallet['add'].value()
                        aux = copy.copy(i)
                        if new != '0.0' or add != '0.0':
                            if new != '0.0' and add != '0.0':
                                fail = "title: 'Error', type: 'error', \
                                    text: 'Solo uno de los campos de monedero \
                                    puede ser rellenado.'"
                            else:
                                if new != '0.0':
                                    i.wallet = new
                                    i.save()
                                else:
                                    i.wallet = float(i.wallet) + float(add)
                                    i.save()
                        else:
                            i.wallet = 0.0
                            i.save()
                        note2 = Notification(reciverCli=i, writer=worker_now,
                                             content="Se ma modificado el \
                                                      monedero del cliente de \
                                                      " + str(aux.wallet) + " \
                                                      a " + str(float(i.wallet)
                                                                ),
                                             typeNote='warning')
                        note2.save()
            wallet = InputMoney()
    else:
        search_clie = SearchClientForm()
        notification = NotificationForm()
        wallet = InputMoney()

    to_return = {'worker_now': worker_now, 'market_now': market_now,
                 'clients': clients, 'search_clie': search_clie,
                 'notification': notification, 'wallet': wallet,
                 'fail': fail}
    return render(request, 'clients.html', to_return)


def take_clients(request):
    data = {}
    if request.method == 'POST':
        worker_now = Worker.objects.get(user__pk=request.POST['user'],
                                        market=request.POST['market'])
        if worker_now.user.is_authenticated:
            if request.POST['operation'] == 'nothing':
                market_now = Market.objects.get(market=request.POST['market'])
                clients = Client.objects.filter(market=market_now)
                serializer = ClientSerializer(clients, many=True)
                data = serializer.data
                return HttpResponse(json.dumps(data))
    data['status'] = 'fail'
    return HttpResponse(json.dumps(data))


@login_required(login_url='/')
def mod_client(request, pk):
    worker_now = Worker.objects.get(user=request.user)
    client = Client.objects.get(pk=pk, market=worker_now.market)
    aux = copy.copy(client)

    if request.method == 'POST':
        new_client = ClientForm(request.POST, request.FILES, instance=client)
        if request.POST['inputInNewCli'] == 'newCli':
            if new_client.is_valid():
                if client.email == '':
                    client.email = None
                client.save()
                note = Notification(reciverCli=client, writer=worker_now,
                                    content="Cliente modificado. \
                                             Datos anteriores; \
                                             Nombre: " + str(aux.name) + "; \
                                             DNI: " + str(aux.dni) + "; \
                                             E-mail: " + str(aux.email) + "; \
                                             Telefono: " + str(aux.tel) + "; \
                                             Monedero: " + str(aux.wallet),
                                    typeNote='normal')
                note.save()
                if aux.wallet != client.wallet:
                    note2 = Notification(reciverCli=client, writer=worker_now,
                                         content="Se ma modificado el \
                                                  monedero del cliente de \
                                                  " + str(aux.wallet) + " a \
                                                  " + str(client.wallet),
                                         typeNote='warning')
                    note2.save()
                return redirect('/client_profile/' + pk)
    else:
        new_client = ClientForm(instance=client)

    to_return = {'new_client': new_client, 'worker_now': worker_now}

    return render(request, 'new_client.html', to_return)


@login_required(login_url='/')
def client_profile(request, pk):
    user_now = request.user
    worker_now = Worker.objects.get(user=user_now)
    market_now = worker_now.market
    client = Client.objects.get(pk=pk, market=market_now)
    sales = Sale.objects.filter(market=market_now, buyer=client)

    notifications = Notification.objects.filter(reciverCli=client,
                                                typeNote='normal')
    warnings_wallet = Notification.objects.filter(reciverCli=client,
                                                  typeNote='warning')

    to_return = {'worker_now': worker_now, 'market_now': market_now,
                 'client': client, 'notifications': notifications,
                 'warningsWallet': warnings_wallet, 'sales': sales}

    return render(request, 'clientProfile.html', to_return)


@login_required(login_url='/')
def delete_client(request, pk):
    worker_now = Worker.objects.get(user=request.user)
    client = Client.objects.get(market=worker_now.market, pk=pk)

    notification = Notification(
        writer=worker_now,
        reciver=worker_now,
        content="<p>Cliente " + client.name + " eliminado satisfactoriamente. \
            DNI: " + client.dni + " \
            Fecha de baja: " + str(datetime.now()) + " \
            Saldo acumulado: " + str(client.wallet) + " ",
        typeNote='normal'
    )
    notification.save()
    client.delete()

    return redirect('/clients')


@login_required(login_url='/')
def index(request):
    worker_now = Worker.objects.get(user=request.user)
    market_now = worker_now.market

    clients = Client.objects.filter(market=market_now)

    products = Product.objects.filter(market=market_now)

    providers = Provider.objects.filter(market=market_now)

    categorys = []
    subcategorys = []

    for i in products:
        counter = 0
        if i.category != '':
            for j in categorys:
                if i.category == j:
                    counter = 1
            if counter == 0:
                categorys.append(i.category)
            else:
                counter = 0
        if i.subcategory != '':
            for j in subcategorys:
                if i.subcategory == j:
                    counter = 1
            if counter == 0:
                subcategorys.append(i.subcategory)

    to_return = {'worker_now': worker_now, 'clients': clients,
                 'products': products, 'providers': providers,
                 'categorys': categorys, 'subcategorys': subcategorys}

    return render(request, 'prueba-index.html', to_return)


def initial_data(request):
    data = {}

    if request.method == 'POST':
        worker_now = Worker.objects.get(user__pk=request.POST['user'])
        if worker_now.user.is_authenticated:
            if request.POST['operation'] == 'nothing':
                aux = Product.objects.filter(
                    market__pk=request.POST['market']
                )
                serializer = ProductSerializer(aux, many=True)
                data = serializer.data
            # return HttpResponse(json.dumps(data))
        else:
            data['status'] = 'fail'
    return HttpResponse(json.dumps(data))


def add_sell(request):
    data = {}
    if request.method == 'POST':
        worker_now = Worker.objects.get(user__pk=request.POST['user'],
                                        market=request.POST['market'])
        if worker_now.user.is_authenticated:
            if request.POST['operation'] == 'addSell':
                list_obj = json.loads(request.POST['products'])

                sale = Sale(market=worker_now.market,
                            seller=worker_now,
                            totAmount=request.POST['totalPrice'],
                            usedWallet=request.POST['usedWallet'],
                            recivedAmount=request.POST['clientMoney'],
                            devolution=request.POST['devolution'],
                            done=True)

                if request.POST['client'] != '':
                    buyer = Client.objects.get(dni=request.POST['client'],
                                               market=worker_now.market)
                    buyer.wallet = buyer.wallet - float(
                        request.POST['usedWallet'])
                    buyer.save()
                    sale.buyer = buyer

                sale.save()
                sale.sale_code = sale.market.name + "#" + str(sale.id)
                sale.save()

                benefice = 0
                for i in list_obj:
                    if 'null' in str(i['pk']):
                        aux_obj = None
                    else:
                        aux_obj = Product.objects.filter(pk=i['pk'])
                        aux_obj = aux_obj[0]

                    sale_prod_aux = ProductSale(
                        product=aux_obj, sale=sale, amount=i['num'],
                        sellPrice=i['price'], totAmount=i['finalPrice']
                    )
                    sale_prod_aux.save()
                    if 'null' not in str(i['pk']):
                        aux_obj.amount = aux_obj.amount - float(
                            sale_prod_aux.amount)
                        aux_obj.save()
                    if 'null' not in str(i['pk']):
                        benefice = (aux_obj.sellPrice - aux_obj.buyPrice)
                        benefice *= i['num']
                sale.benefice = benefice
                sale.save()
                # GENERAR NOTIFICACION
                data['location'] = request.META['HTTP_REFERER']
                return HttpResponse(json.dumps(data))

    data['status'] = 'fail'
    return HttpResponse(json.dumps(data))


@login_required(login_url='/')
def cash_flows(request):
    worker_now = Worker.objects.get(user=request.user)
    market_now = worker_now.market

    sales = Sale.objects.filter(market=market_now)
    sales_of_the_day = []
    # print date.today() #.isoformat()

    for i in sales:
        if i.date.date() == date.today():
            sales_of_the_day.append(i)

    tot_by_seller = []
    aux = {}
    counter = 0

    for i in sales_of_the_day:
        if tot_by_seller == []:
            aux['seller'] = i.seller.user.username
            aux['image'] = i.seller.image
            aux['amount'] = i.totAmount
            aux['sales'] = 1
            tot_by_seller.append(aux)
        else:
            counter = 0
            for j in tot_by_seller:
                if i.seller.user.username == j['seller']:
                    j['amount'] = j['amount'] + i.totAmount
                    j['sales'] = j['sales'] + 1
                    counter = 1
                    break
            if counter == 0:
                aux = {}
                aux['seller'] = i.seller.user.username
                aux['image'] = i.seller.image
                aux['amount'] = i.totAmount
                aux['sales'] = 1
                tot_by_seller.append(aux)

    to_return = {'worker_now': worker_now, 'salesOfTheDay': sales_of_the_day,
                 'totBySeller': tot_by_seller}

    return render(request, 'cashFlow.html', to_return)


# Only takes last 7 days (Optimal For Graph)
@csrf_exempt
def take_sales(request):
    if request.method == 'POST':
        if request.POST['operation'] == 'takeSales':
            worker_now = Worker.objects.get(
                user__pk=request.POST['user'],
                market__pk=request.POST['market']
            )
            if worker_now.user.is_authenticated:
                market_now = worker_now.market
                sales = Sale.objects.filter(market=market_now)
                aux = []
                for i in sales:
                    if abs(sales.last().date - i.date).days <= 7:
                        aux.append(i)

                serializer = SaleSerializer(aux, many=True)
                print serializer
                data = serializer.data
                print json.dumps(data)
            else:
                data['redirect'] = request.META['HTTP_ORIGIN']
        else:
            data['status'] = 'fail'
    else:
        data['status'] = 'fail'
    return HttpResponse(json.dumps(data))


@login_required(login_url='/')
def all_sales(request):
    worker_now = Worker.objects.get(user=request.user)
    aux = Sale.objects.filter(market=worker_now.market)

    sales = list(aux)
    sales.reverse()

    products = Product.objects.filter(market=worker_now.market)
    categorys = []

    for i in products:
        counter = 0
        if i.category != '':
            for j in categorys:
                if i.category == j:
                    counter = 1
            if counter == 0:
                categorys.append(i.category)

    to_return = {'worker_now': worker_now, 'categorys': categorys,
                 'sales': sales}
    return render(request, 'sales.html', to_return)
