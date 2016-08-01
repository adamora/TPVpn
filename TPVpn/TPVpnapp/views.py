#encoding:utf-8
from django.shortcuts import render, redirect, render_to_response
from TPVpnapp.models import *
from django.contrib.auth import login, authenticate, logout
from TPVpnapp.forms import *
from django.forms import modelformset_factory,formset_factory
from django.contrib.auth.decorators import login_required
from datetime import datetime,date
from django.template import RequestContext
import copy

from django.core.serializers.json import json
from django.core import serializers
from TPVpnapp.serializers import *

import json
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def logAndReg(request):
	if not request.user.is_anonymous():
		return redirect('/index')
	if request.method=='POST':
		loginuser=LoginForm(data=request.POST)
		newuser=UserForm(request.POST)
		neworker=RegisterWorker(request.POST)
		newbusiness=RegisterBusinessForm(request.POST)
		newAddress=RegisterFullDirectionForm(request.POST)

		if request.POST['inputInLogin']=='loginUser':
			if loginuser.is_valid():
				user=request.POST.get('username',False)
				key=request.POST.get('password',False)
				return newLogin(request,user,key)
			else: #--> DJANGO SE ENCARGA DE LOS ERRORES EN LA INTRODUCCIÓN DE DATOS
				print "¡FALLO EN LA OBTENCIÓN DEL LOGIN!"
			#	return render(request,'page_404.html')
		if request.POST['inputInLogin'] == 'registerMarket':
			if newAddress.is_valid():
				addr = newAddress.save() #Guardamos el objeto Direccion obtenido del formulario
			else:
				print "NO SE HA PODIDO GUARDAR DIRECCION"
			if newbusiness.is_valid():
				if (request.POST.get('secretKey', True) == request.POST.get('secretKey2', True)):
					business = newbusiness.save(commit=False)
					business.direction = addr
					business.save()
					return redirect('/login') #Aunque debería poder mandar a una pagina de "EXITO"
				else:
					return "NO SE HA PODIDO CREAR MERCADO"
	else:
		newuser=UserForm()
		neworker=RegisterWorker()
		loginuser=LoginForm()
		newAddress=RegisterFullDirectionForm()
		newbusiness=RegisterBusinessForm()
	return render(request,'login.html',{'loginuser':loginuser, 'newAddress':newAddress, 'newbusiness':newbusiness})

@login_required(login_url='/')
def neWorker(request):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	if request.method=='POST':
		newuser = UserForm(request.POST)
		neworker = RegisterWorker(request.POST,request.FILES)
		newAddress = RegisterFullDirectionForm(request.POST)
		password = PasswordMarketForm(request.POST)
		if request.POST['neWorkerForm']=='registerUser':
			if newuser.is_valid() * newAddress.is_valid() * neworker.is_valid() * password.is_valid():
				if request.POST.get('secretKey',False) == marketNow.secretKey:
					userAux = newuser.save()
					''' >>>>> FUNCIONA PARO NO UTIL -> NO LOGIN
					user = request.POST.get('username',False)
					key = request.POST.get('password1',False)
					'''
					addr = newAddress.save()
					workerAux = neworker.save(commit=False)
					workerAux.user = userAux
					workerAux.market = marketNow
					workerAux.home = addr
					workerAux.save()
					return redirect('/employers')
				else:
					password['secretKey'].error = "¡Contraseña incorrecta!"
			elif newuser.is_valid() == False:
				print "NO SE HA CREADO BIEN EL USER"
			elif not newAddress.is_valid():
				print "NO SE HA CREADO BIEN LA DIRECCIÓN"
			elif not neworker.is_valid():
				print "NO SE HA CREADO BIEN EL USUARIO"
			else:
				print "¡ERROR! CONTACTE CON EL SERVICIO TÉCNICO"
				return render(request,'page_404.html')

	else:
		newuser = UserForm()
		neworker = RegisterWorker()
		newAddress = RegisterFullDirectionForm()
		password = PasswordMarketForm()
	return render(request,'workerForm.html',{'newuser':newuser, 'neworker':neworker, 'newAddress':newAddress, 'workerNow':workerNow, 'password':password})

@login_required(login_url='/')
def listWorkers(request):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market

	fail = None
	workers = Worker.objects.filter(market=marketNow)

	if request.method == 'POST':
		search = SearchWorkerForm(request.POST)
		notification = NotificationForm(request.POST)
		if 'searchWorkerForm' in request.POST:
			if request.POST['searchWorkerForm'] == 'searchWorker':
				if search.is_valid():
					aux = request.POST.get('array',False)
					cad = aux.split(' ')
					auxC = []
					for word in cad:
						auxN = Worker.objects.filter(user__first_name__icontains=word,market=marketNow)
						auxA = Worker.objects.filter(user__last_name__icontains=word, market=marketNow)
						auxL = Worker.objects.filter(user__username__icontains=word, market=marketNow)
						auxD = Worker.objects.filter(dni__icontains=word, market=marketNow)
						if auxN or auxA or auxL or auxD:
							for i in list(auxN) + list(auxA) + list(auxL) + list(auxD):
								counter = 0
								for j in auxC:
									if i==j:
										counter=1
								if counter == 0:
									if i:
										auxC.append(i)
					if auxC:
						workers = auxC
					else:
						fail = "title: 'Error', type: 'error', text: 'No se han encontrado trabajadores.'"
		if 'newNotification' in request.POST:
			for i in workers:
				if request.POST['newNotification'] == i.dni:
					if notification.is_valid():
						aux = notification.save(commit=False)
						aux.reciver = i
						aux.writer = workerNow
						aux.typeNote = 'normal'
						aux.save()
						notification = NotificationForm()
	else:
		search = SearchWorkerForm()
		notification = NotificationForm()

	to_return = {
		'workerNow':workerNow,
		'workers':workers,
		'search':search,
		'notification':notification,
		'fail':fail
	}
	return render(request,'employers.html',to_return)

@login_required(login_url='/')
def modWorker(request,pk):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	fail = None

	workerProfile = Worker.objects.get(dni=pk)

	if workerProfile == workerNow:
		if request.method == 'POST':
			newuser = UserForm(request.POST,instance=workerProfile.user)
			neworker = RegisterWorker(request.POST,instance=workerProfile)
			newAddress = RegisterFullDirectionForm(request.POST,instance=workerProfile.home)
			password = PasswordMarketForm(request.POST)
			if request.POST['neWorkerForm']=='registerUser':
				if newuser.is_valid() * newAddress.is_valid() * neworker.is_valid() * password.is_valid():
					if request.POST.get('secretKey',False) == marketNow.secretKey:
						userAux = newuser.save()
						addr = newAddress.save()
						workerAux = neworker.save(commit=False)
						if request.POST.get('genre', False) == False:
							workerAux.genre = workerProfile.genre
						workerAux.user = userAux
						workerAux.market = marketNow
						workerAux.home = addr
						workerAux.save()
						return newLogin(request,workerAux.user.username,request.POST.get('password1',False))
					else:
						password['secretKey'].error = "¡Contraseña incorrecta!"

		else:
			newuser = UserForm(instance=workerProfile.user)
			neworker = RegisterWorker(instance=workerProfile)
			newAddress = RegisterFullDirectionForm(instance=workerProfile.home)
			password = PasswordMarketForm()

		to_return = {
			'workerNow':workerNow,
			'fail':fail,
			'newuser':newuser,
			'neworker':neworker,
			'newAddress':newAddress,
			'password':password
		}
	else:
		return redirect('/employers')

	return render(request,'workerForm.html',to_return)

@login_required(login_url='/')
def workerProfile(request,pk):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	fail = None

	workerProfile = Worker.objects.get(dni=pk)
	notifications = Notification.objects.filter(reciver=workerProfile)

	to_return = {
		'workerNow':workerNow,
		'workerProfile':workerProfile,
		'notifications':notifications,
		'fail':fail
	}

	return render(request,'employerProfile.html',to_return)


def newLogin(request,user,key):
	print "El usuario ", user," intenta iniciar sesión."
	access=authenticate(username=user,password=key)
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
def logoutSession(request):
	logout(request)
	return redirect('/')


@login_required(login_url='/') #REVISADO
def newProduct(request):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	if request.method == 'POST':
		newprovider = ProviderForm(request.POST)
		newprod = ProductForm(request.POST,request.FILES)
		if request.POST['inputInNewProd'] == 'newProvider':
			if newprovider.is_valid():
				if not Provider.objects.filter(
					namePro=newprovider['namePro'].value(),
					market=workerNow.market
				):
					provider = newprovider.save(commit=False)
					provider.market = workerNow.market
					provider.save()
				else:
					provider = Provider.objects.get(
						namePro=newprovider['namePro'].value(),
						market=workerNow.market
					)
				newprod = ProductForm(initial={'provider':provider})
				newprovider = ProviderForm(instance=provider)
		elif request.POST['inputInNewProd'] == 'newProd':
			if newprod.is_valid():
				prod = newprod.save(commit=False)
				prod.market = workerNow.market
				prod.offer = prod.sellPrice
 				if prod.barCode == '':
					prod.barCode = 'Vacio'
				if newprod['image'].value() != None:
					newprod['image'].error = 'Vuelva a seleccionar la imagen.'
				if prod.buyPrice > prod.sellPrice:
					newprod['sellPrice'].error = '¡El precio de venta no puede ser superior al de compra!'
				elif prod.amount < 0:
					newprod['amount'].error = '¡La cantidad de producto debe ser mayor a 0!'
				else:
					prod.save()
					return redirect('/new_product')
			else:
				print "¡Error!: No se han cumplimentado correctamente los datos del producto."
	else:
		newprovider = ProviderForm()
		newprod = ProductForm()

	to_return = {
		'workerNow':workerNow,
		'newprovider':newprovider,
		'newprod':newprod
	}

	return render(request,'productForm.html',to_return)

@login_required(login_url='/')
def listProducts(request): #REVISADO
	workerNow = Worker.objects.get(user=request.user)
	marketNow = workerNow.market
	products = Product.objects.filter(market=marketNow)
	fail = None

	if request.method == 'POST':
		searchProduct = SearchProduct(request.POST)
		modQuantity = StockForm(request.POST)
		if 'searching' in request.POST:
			if request.POST['searching'] == 'searchProd':
				if searchProduct.is_valid():
					aux = searchProduct['search'].value()
					if aux != '':
						cad = aux.split(' ')
						auxCad = []
						for word in cad:
							auxN = Product.objects.filter(name__icontains=word, market=marketNow)
							auxB = Product.objects.filter(brand__icontains=word, market=marketNow)
							auxP = Product.objects.filter(provider__namePro__icontains=word, market=marketNow)
							auxC = Product.objects.filter(category__icontains=word, market=marketNow)
							auxSC = Product.objects.filter(subcategory__icontains=word, market=marketNow)
							auxBC = Product.objects.filter(barCode__icontains=word, market=marketNow)
							if auxN or auxB or auxP or auxC or auxSC or auxBC:
								for i in list(auxN) + list(auxB) + list(auxP) + list(auxC) + list(auxSC) + list(auxBC):
									counter = 0
									for j in auxCad:
										if i==j:
											counter = 1
									if counter == 0:
										if i:
											auxCad.append(i)
						if not auxCad:
							fail = "title: 'Error', type: 'error', text: 'No se han encontrado productos.'"
						else:
							products = auxCad
		if 'newQuantity' in request.POST:
			for i in products:
				if request.POST['newQuantity'] == str(i.pk):
					if modQuantity.is_valid():
						if modQuantity['new'].value() != '' and modQuantity['add'].value() != '':
							modQuantity['new'].error = '¡Error! Ambos campos no pueden ser cumplimentados.'
							fail = "title: 'Error', type: 'error', text: 'Ambos campos de stock en <big><b>" + i.name + "</b></big> no pueden ser cumplimentados.'"
						elif modQuantity['new'].value() != '':
							if float(modQuantity['new'].value()) < 0:
								modQuantity['new'].error = '¡Error! El valor debe ser mayor o igual a cero.'
								fail = "title: 'Error', type: 'error', text: 'El valor introducido en <big><b>" + i.name + "</b></big> debe ser mayor o igual a cero.'"
							else:
								i.amount = modQuantity['new'].value()
								i.save()
						elif modQuantity['add'].value() != '':
							i.amount = i.amount + float(modQuantity['add'].value())
							i.save()
						else:
							modQuantity['new'].error = '¡Error! Uno de los campos debe ser cumplimentado.'
							fail = "title: 'Aviso', type: 'warning', text: 'Uno de los campos de stock en <big><b>" + i.name + "</b></big> debe ser cumplimentado.'"
					#modQuantity = StockForm()
	else:
		searchProduct = SearchProduct()
		modQuantity = StockForm()

	to_return = {
		'workerNow':workerNow,
		'marketNow':marketNow,
		'products':products,
		'searchProduct':searchProduct,
		'modQuantity':modQuantity,
		'fail':fail
	}

	return render(request,'products.html',to_return)

@login_required(login_url='/')
def deleteProduct(request,product_id): #REVISADO
	workerNow = Worker.objects.get(user=request.user)
	marketNow = workerNow.market
	product = Product.objects.get(id=product_id,market=marketNow)

	if product:
		product.delete()
	#else:
		#AGREGAR UNA NOTIFICACION AL USUARIO
	return redirect('/products')

@login_required(login_url='/')
def modifyProduct(request,product_id): #REVISADO
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	product = Product.objects.get(id=product_id,market=workerNow.market)
	if request.method == 'POST':
		newprovider = ProviderForm(request.POST)
		newprod = ProductForm(request.POST,request.FILES,instance=product)
		if request.POST['inputInNewProd'] == 'newProvider':
			if newprovider.is_valid():
				provider = newprovider.save(commit=False)
				provider.market = workerNow.market
				provider.save()
				product.provider = provider
				product.save()
				return redirect('/modProd/' + product_id)
		if request.POST['inputInNewProd'] == 'newProd':
			if newprod.is_valid():
				prod = newprod.save(commit=False)
				prod.offer = prod.sellPrice
 				if prod.barCode == '':
					prod.barCode = 'Vacio'
				if prod.buyPrice > prod.sellPrice:
					newprod['sellPrice'].error = '¡El precio de venta no puede ser superior al de compra!'
				elif prod.amount < 0:
					newprod['amount'].error = '¡La cantidad de producto debe ser mayor a 0!'
				else:
					prod.save()
					return redirect('/products')
			else:
				print "¡Error!: No se han cumplimentado correctamente los datos del producto."
	else:
		newprovider = ProviderForm()
		newprod = ProductForm(instance=product)
	return render(request,'productForm.html',{'workerNow':workerNow,'newprovider':newprovider,'newprod':newprod}, context_instance=RequestContext(request))


@login_required(login_url='/')
def newClient(request):
	workerNow = Worker.objects.get(user=request.user)

	if request.method == 'POST':
		newClient = ClientForm(request.POST,request.FILES)
		if request.POST['inputInNewCli'] == 'newCli':
			if newClient.is_valid():
				auxCli = newClient.save(commit=False)
				auxCli.market = workerNow.market
				if auxCli.email=='':
					auxCli.email = None
				auxCli.save()
				return redirect('/clients')
	else:
		newClient = ClientForm()

	to_return = {
		'newClient':newClient,
		'workerNow':workerNow
	}

	return render(request,'newClient.html',to_return)

@login_required(login_url='/')
def listClients(request):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	clients = Client.objects.filter(market=marketNow)
	fail = None

	if request.method == 'POST':
		searchClie = SearchClientForm(request.POST)
		notification = NotificationForm(request.POST)
		wallet = InputMoney(request.POST)
		if 'searchCli' in request.POST:
			if request.POST['searchCli'] == 'newSearch':
				if searchClie.is_valid():
					aux = searchClie['array'].value()
					if aux != '':
						cad = aux.split(' ')
						listAux = []
						for word in cad:
							auxN = Client.objects.filter(name__icontains=word, market=marketNow)
							auxD = Client.objects.filter(dni__icontains=word, market=marketNow)
							auxE = Client.objects.filter(email__icontains=word, market=marketNow)
							if auxN or auxD or auxE:
								for i in list(auxN) + list(auxD) + list(auxE):
									counter = 0
									for j in listAux:
										if i == j:
											counter = 1
									if counter == 0:
										if i:
											listAux.append(i)
						if not listAux:
							fail = "title: 'Error', type: 'error', text: 'No se han encontrado clientes.'"
						else:
							clients = listAux
		if 'newNotification' in request.POST:
			for i in clients:
				if request.POST['newNotification'] == i.pk:
					if notification.is_valid():
						noteAux = notification.save(commit=False)
						noteAux.writer = workerNow
						noteAux.reciverCli = i
						noteAux.typeNote = 'normal'
						noteAux.save()
						notification = NotificationForm()
		if 'modWallet' in request.POST: ########## ARREGLAR
			for i in clients:
				if request.POST['modWallet'] == i.pk:
					if wallet.is_valid():
						new = wallet['new'].value()
						add = wallet['add'].value()
						aux = copy.copy(i)
						if new != '0.0' or add != '0.0':
							if new != '0.0' and add != '0.0':
								fail = "title: 'Error', type: 'error', \
									text: 'Solo uno de los campos de monedero puede ser rellenado.'"
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
						note2 = Notification(
							reciverCli = i,
							writer = workerNow,
							content = "Se ma modificado el monedero del cliente de \
							" + str(aux.wallet) + " a " + str(float(i.wallet)),
							typeNote = 'warning'
						)
						note2.save()
			wallet = InputMoney()
	else:
		searchClie = SearchClientForm()
		notification = NotificationForm()
		wallet = InputMoney()

	to_return = {
		'workerNow':workerNow,
		'marketNow':marketNow,
		'clients':clients,
		'searchClie':searchClie,
		'notification':notification,
		'wallet':wallet,
		'fail':fail
	}
	return render(request,'clients.html',to_return)

@csrf_exempt
def takeClients(request):
	data = {}
	if request.method == 'POST':
		workerNow = Worker.objects.get(
			user__pk = request.POST['user'],
			market = request.POST['market']
		)
		if workerNow.user.is_authenticated:
			if request.POST['operation'] == 'nothing':
				marketNow = Market.objects.get(market=request.POST['market'])
				clients = Client.objects.filter(market=marketNow)
				serializer = ClientSerializer(clients,many=True)
				data = serializer.data
				return HttpResponse(json.dumps(data))
	data['status'] = 'fail'
	return HttpResponse(json.dumps(data))

@login_required(login_url='/')
def modClient(request,pk):
	workerNow = Worker.objects.get(user=request.user)
	client = Client.objects.get(pk=pk,market=workerNow.market)
	aux = copy.copy(client)

	if request.method == 'POST':
		newClient = ClientForm(request.POST,request.FILES,instance=client)
		if request.POST['inputInNewCli'] == 'newCli':
			if newClient.is_valid():
				if client.email == '':
					client.email = None
				client.save()
				note = Notification(
					reciverCli = client,
					writer = workerNow,
					content = "Cliente modificado. Datos anteriores; \
						Nombre: "+str(aux.name)+"; DNI: "+str(aux.dni)+"; \
						E-mail: "+str(aux.email)+"; Telefono: "+str(aux.tel)+"; \
						Monedero: " + str(aux.wallet),
					typeNote = 'normal'
				)
				note.save()
				if aux.wallet != client.wallet:
					note2 = Notification(
						reciverCli = client,
						writer = workerNow,
						content = "Se ma modificado el monedero del cliente de \
						" + str(aux.wallet) + " a " + str(client.wallet),
						typeNote = 'warning'
					)
					note2.save()
				return redirect('/client_profile/'+pk)
	else:
		newClient = ClientForm(instance=client)

	to_return = {
		'newClient':newClient,
		'workerNow':workerNow
	}

	return render(request,'newClient.html',to_return)

@login_required(login_url='/')
def clientProfile(request,pk):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	client = Client.objects.get(pk=pk,market=marketNow)
	sales = Sale.objects.filter(market=marketNow,buyer=client)

	notifications = Notification.objects.filter(reciverCli=client, typeNote='normal')
	warningsWallet = Notification.objects.filter(reciverCli=client, typeNote='warning')

	to_return = {
		'workerNow':workerNow,
		'marketNow':marketNow,
		'client':client,
		'notifications':notifications,
		'warningsWallet':warningsWallet,
		'sales':sales
	}

	return render(request,'clientProfile.html',to_return)

@login_required(login_url='/')
def deleteClient(request,pk):
	workerNow = Worker.objects.get(user=request.user)
	client = Client.objects.get(market=workerNow.market,pk=pk)

	notification = Notification(
		writer = workerNow,
		reciver = workerNow,
		content = "<p>Cliente " + client.name+ " eliminado satisfactoriamente. \
			DNI: " + client.dni + " \
			Fecha de baja: " + str(datetime.now()) + " \
			Saldo acumulado: " + str(client.wallet) + " ",
		typeNote = 'normal'
	)
	notification.save()
	client.delete()

	return redirect('/clients')


@login_required(login_url='/')
def index(request):
	workerNow = Worker.objects.get(user=request.user)
	marketNow = workerNow.market

	clients = Client.objects.filter(market=marketNow)

	products = Product.objects.filter(market=marketNow)

	providers = Provider.objects.filter(market=marketNow)


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

	to_return = {
		'workerNow':workerNow,
		'clients':clients,
		'products':products,
		'providers':providers,
		'categorys':categorys,
		'subcategorys':subcategorys
	}
	return render(request,'prueba-index.html',to_return)

@csrf_exempt
def initialData(request):
	data = {}
	if request.method == 'POST':
		workerNow = Worker.objects.get(user__pk=request.POST['user'])
		if workerNow.user.is_authenticated:
			if request.POST['operation'] == 'nothing':
				aux = Product.objects.filter(
					market__pk=request.POST['market']
				)
				serializer = ProductSerializer(aux,many=True)
				data = serializer.data
			return HttpResponse(json.dumps(data))
		else:
			data['status'] = 'fail'
			return HttpResponse(json.dumps(data))

@csrf_exempt
def addSell(request):
	data = {}
	if request.method == 'POST':
		workerNow = Worker.objects.get(
			user__pk = request.POST['user'],
			market = request.POST['market']
		)
		if workerNow.user.is_authenticated:
			if request.POST['operation'] == 'addSell':
				listObj = json.loads(request.POST['products'])
				#>>>>>> comprobar listObj -> si no tiene productos, error

				sale = Sale(
					market = workerNow.market,
					seller = workerNow,
					totAmount = request.POST['totalPrice'],
					usedWallet = request.POST['usedWallet'],
					recivedAmount = request.POST['clientMoney'],
					devolution = request.POST['devolution'],
					done = True
				)

				if request.POST['client'] != '':
					buyer = Client.objects.get(
						dni=request.POST['client'],
						market= workerNow.market
					)
					buyer.wallet = buyer.wallet - float(request.POST['usedWallet'])
					buyer.save()
					sale.buyer = buyer

				sale.save()
				sale.sale_code = sale.market.name +"#"+ str(sale.id)
				sale.save()

				benefice = 0
				for i in listObj:
					if 'null' in str(i['pk']): #CONTROLAR ESTO
						auxObj = None
					else:
						auxObj = Product.objects.filter(pk=i['pk'])
						auxObj = auxObj[0]

					saleProdAux = ProductSale(
						product = auxObj, sale = sale, amount = i['num'],
						sellPrice = i['price'], totAmount = i['finalPrice']
					)
					saleProdAux.save()
					if not 'null' in str(i['pk']):
						auxObj.amount = auxObj.amount - float(saleProdAux.amount)
						auxObj.save()
					#Beneficio para agregar a sale
					if 'null' not in str(i['pk']): #CONTROLAR ESTO
						benefice = (auxObj.sellPrice - auxObj.buyPrice) *i['num']
				sale.benefice = benefice
				sale.save()
				#GENERAR NOTIFICACION
				data['location'] = request.META['HTTP_ORIGIN'] + '/index'
				return HttpResponse(json.dumps(data)) ##que se lo traga el cabron

	data['status'] = 'fail'
	return HttpResponse(json.dumps(data))

@login_required(login_url='/')
def cashFlows(request):
	workerNow = Worker.objects.get(user=request.user)
	marketNow = workerNow.market

	sales = Sale.objects.filter(market = marketNow)
	salesOfTheDay = []
	#print date.today() #.isoformat()

	for i in sales:
		if i.date.date() == date.today():
			salesOfTheDay.append(i)

	totBySeller = []
	aux = {}
	counter = 0

	for i in salesOfTheDay:
		if totBySeller == []:
			aux['seller'] = i.seller.user.username
			aux['image'] = i.seller.image
			aux['amount'] = i.totAmount
			aux['sales'] = 1
			totBySeller.append(aux)
		else:
			counter = 0
			for j in totBySeller:
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
				totBySeller.append(aux)

	to_return = {
		'workerNow':workerNow,
		'salesOfTheDay':salesOfTheDay,
		'totBySeller':totBySeller
	}

	return render(request,'cashFlow.html',to_return)

@csrf_exempt
def takeSales(request): #Only takes last 7 days (Optimal For Graph)
	if request.method == 'POST':
		if request.POST['operation'] == 'takeSales':
			workerNow = Worker.objects.get(
				user__pk=request.POST['user'],
				market__pk=request.POST['market']
			)
			if workerNow.user.is_authenticated:
				marketNow = workerNow.market
				sales = Sale.objects.filter(market=marketNow)
				aux = []
				for i in sales:
					if abs(sales.last().date - i.date).days <= 7 :
						aux.append(i)

				serializer = SaleSerializer(aux,many=True)
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
def allSales(request):
	workerNow = Worker.objects.get(user=request.user)
	aux = Sale.objects.filter(market=workerNow.market)

	sales = list(aux)
	sales.reverse()

	products = Product.objects.filter(market=workerNow.market)
	categorys = []

	for i in products:
		counter = 0
		if i.category != '':
			for j in categorys:
				if i.category == j:
					counter = 1
			if counter == 0:
				categorys.append(i.category)

	to_return = {
		'workerNow':workerNow,
		'categorys':categorys,
		'sales':sales
	}
	return render(request,'sales.html',to_return)