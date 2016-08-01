

@login_required(login_url='/')
def mainPage(request): #HACER FUNCION COMON SALE PARA mainPage y actualSale
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market

	date = datetime.now()
	oldProds = None
	fail = None

	for i in Sale.objects.filter(totAmount=0.0):
		if not ProductBill.objects.filter(sale=i):
			i.delete()

	#PARA AGREGAR PRODUCTOS POR PRIMERA VEZ A FACTURA
	sale = Sale()
	sale.done = False
	sale.market = marketNow
	sale.seller = workerNow
	#sale.sale_code = marketNow.name + str(sale.id)
	#sale.save()
	for i in Sale.objects.all():
		j = i

	if not Sale.objects.all():
		sale_code = 0
	else:
		sale_code = j.sale_code[len(marketNow.name)+1:]
		sale_code = int(sale_code) + 1

	sale.sale_code = marketNow.name + "#" + str(sale_code)
	sale.save()

	#AGREGAR PRIMER PRODUCTO
	if request.method == 'POST':
		addProd = ProductBillForm(request.POST)
		searchBill = SearchBillForm(request.POST)
		searchCli = SearchCliForm(request.POST)
		#recivedAmount = InputMoney(request.POST)
		if request.POST['inputProduct'] == 'addProduct':
			if addProd.is_valid():
				newAdded = addProd.save(commit=False)
				fail = addToSale(newAdded,sale)

				if fail:
					#VARIABLES A DEVOLVER
					to_return = {
						'workerNow':workerNow,
						'oldProds':oldProds,
						'date':date,
						'market':marketNow,
						'sale':sale,
						'addProd':addProd,
						'fail':fail,
						'searchBill':searchBill,
						'searchCli':searchCli
					}
					return render(request,'index.html',to_return)
				else:
					return redirect('/index/' + str(sale.id))
		if request.POST['inputProduct'] == 'searchBill':
			if searchBill.is_valid():
				bill = request.POST.get('sale_code',False)
				if Sale.objects.filter(sale_code=bill) and (sale.market == workerNow.market):
					saleSearch = Sale.objects.get(sale_code=bill)
					return redirect('/index/' + str(saleSearch.id))
				else:
					fail = "¡Error!: La factura buscada no existe."
					#VARIABLES A DEVOLVER
					to_return = {
						'workerNow':workerNow,
						'oldProds':oldProds,
						'date':date,
						'market':marketNow,
						'sale':sale,
						'addProd':addProd,
						'fail':fail,
						'searchBill':searchBill,
						'searchCli':searchCli
					}
					return render(request,'index.html',to_return)
		if request.POST['inputProduct'] == 'takeClient':
			if searchCli.is_valid():
				searchedCli = searchCli.save(commit=False)
				sale.buyer = searchedCli.buyer
				sale.save()
				return redirect('/index/' + str(sale.id))
	else:
		addProd = ProductBillForm()
		searchBill = SearchBillForm()
		searchCli = SearchCliForm()

	#VARIABLES A DEVOLVER
	to_return = {
		'workerNow':workerNow,
		'oldProds':oldProds,
		'date':date,
		'market':marketNow,
		'sale':sale,
		'addProd':addProd,
		'fail':fail,
		'searchBill':searchBill,
		'searchCli':searchCli
	}
	return render(request,'index.html',to_return)

@login_required(login_url='/')
def actualSale(request,sale_id):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	fail = None
	#mixList = None

	sale = Sale.objects.get(id=sale_id)
	if not marketNow == sale.market:
		fail = "¡El código de factura no corresponde a esta tienda!"
		return render(request,'index.html',{'workerNow':workerNow,'oldProds':oldProds,'date':date, 'market':marketNow, 'sale':sale,'addProd':addProd,'fail':fail,'mixList':mixList})

	date = sale.date
	oldProds = ProductBill.objects.filter(sale=sale)
	if not oldProds:
		oldProds = None

	PBFormSet = modelformset_factory(ProductBill, form=ProductBillForm,extra=0)
	listModifyProd = PBFormSet(queryset=oldProds)

	if not oldProds:
		mixList = None
	else:
		mixList = zip(listModifyProd,oldProds)#----------------->PROBARLO A PONERLO DELANTE DE TODO

	if request.method == 'POST':
		listModifyProd = PBFormSet(request.POST,prefix='pfix')
		addProd = ProductBillForm(data=request.POST)
		#mixList = zip(modifyProd,oldProds)#
		searchBill = SearchBillForm(request.POST)
		searchCli = SearchCliForm(request.POST)
		takeAmount = InputMoney(request.POST)
		recivedAmount = InputMoney(request.POST)
		done = InputTrue(request.POST)
		if request.POST['inputProduct'] == 'modifyProd':################### ARREGLAR
			if listModifyProd.is_valid():
				#EMPEZAR EL FOR
				for modifyProd in listModifyProd:
					aux = modifyProd.save(commit=False)
					PBaux = ProductBill.objects.get(id=aux.id)
					product = Product.objects.get(id=aux.product.id)
					if not PBaux.amount == aux.amount:
						if product.amount >= aux.amount:
							if not PBaux.sellPrice == aux.sellPrice:
								sale.totAmount = sale.totAmount - PBaux.sellPrice + aux.sellPrice
								aux.totAmount = aux.sellPrice * aux.amount
							product.amount = product.amount + PBaux.amount
							product.amount = product.amount - aux.amount
							product.save()
							PBaux.delete()
							aux.save()
						else:
							fail = "¡Error!: Quedan " + str(price.amount) + " " + str(price.product.kind)
							return render(request,'index.html',{'workerNow':workerNow,'oldProds':oldProds,'date':date, 'market':marketNow, 'sale':sale,'addProd':addProd,'fail':fail,'mixList':mixList,'searchBill':searchBill,'searchCli':searchCli,'takeAmount':takeAmount,'recivedAmount':recivedAmount})
					elif not PBaux.sellPrice == aux.sellPrice:
						sale.totAmount = sale.totAmount - PBaux.sellPrice + aux.sellPrice
						aux.totAmount = aux.sellPrice * aux.amount
						PBaux.delete()
						aux.save()
					#<<<<<<<<<<<<<<<<<<<<<<< ACABA ARREGLAR
		if request.POST['inputProduct'] == 'addProduct':
			if addProd.is_valid():
				newAdded = addProd.save(commit=False)

				if not oldProds == None:
					for i in oldProds:
						if newAdded.product == i.product:
							return redirect('/index/' + str(sale.id))

				fail = addToSale(newAdded,sale)

				if fail:
					return render(request,'index.html',{'workerNow':workerNow,'oldProds':oldProds,'date':date, 'market':marketNow, 'sale':sale,'addProd':addProd,'fail':fail,'mixList':mixList,'searchBill':searchBill,'searchCli':searchCli,'takeAmount':takeAmount,'recivedAmount':recivedAmount})
				else:
					return redirect('/index/' + str(sale.id))
		if request.POST['inputProduct'] == 'searchBill':
			if searchBill.is_valid():
				bill = request.POST.get('sale_code',False)
				if Sale.objects.filter(sale_code=bill) and (sale.market == workerNow.market):
					saleSearch = Sale.objects.get(sale_code=bill)
					return redirect('/index/' + str(saleSearch.id))
				else:
					fail = "¡Error!: La factura buscada no existe."
					return render(request,'index.html',{'workerNow':workerNow,'oldProds':oldProds,'date':date, 'market':marketNow, 'sale':sale,'addProd':addProd,'fail':fail,'mixList':mixList,'searchBill':searchBill,'searchCli':searchCli,'takeAmount':takeAmount,'recivedAmount':recivedAmount})
		if request.POST['inputProduct'] == 'takeClient':
			if searchCli.is_valid():
				searchedCli = searchCli.save(commit=False)
				sale.buyer = searchedCli.buyer
				sale.save()
				return redirect('/index/' + str(sale.id))
		if request.POST['inputProduct'] == 'takeAmount': ###########>>>>>>>>>>COMPROBAR
			if takeAmount.is_valid():
				auxAmount = takeAmount.save(commit=False)
				if sale.buyer.wallet < auxAmount.wallet:
					fail = '¡Error!: La cantidad introducida es superior al monedero.'
					to_return = {
						'workerNow':workerNow,
						'oldProds':oldProds,
						'date':date,
						'market':marketNow,
						'sale':sale,
						'addProd':addProd,
						'fail':fail,
						'mixList':mixList,
						'searchBill':searchBill,
						'searchCli':searchCli,
						'takeAmount':takeAmount,
						'recivedAmount':recivedAmount
					}
					return render(request,'index.html',to_return)
				else:
					buyer = Client.objects.get(pk=sale.buyer.pk)
					buyer.wallet = buyer.wallet - auxAmount.wallet
					sale.totAmount = sale.totAmount - auxAmount.wallet
					sale.usedWallet = auxAmount.wallet
					if sale.recivedAmount > 0:
						sale.devolution = sale.devolution - sale.usedWallet
					buyer.save()
					sale.save()
					return redirect('/index/' + str(sale.id))
		if request.POST['inputProduct'] == 'recAmount':
			if recivedAmount.is_valid():
				aux = recivedAmount.save(commit=False)
				sale.recivedAmount = aux.wallet
				#sale.save()
				if sale.recivedAmount >= sale.totAmount:
					sale.devolution = sale.totAmount - sale.recivedAmount
				else:
					fail = "El importe obtenido es insuficiente."
					to_return = {
						'workerNow':workerNow,
						'oldProds':oldProds,
						'date':date,
						'market':marketNow,
						'sale':sale,
						'addProd':addProd,
						'fail':fail,
						'mixList':mixList,
						'searchBill':searchBill,
						'searchCli':searchCli,
						'takeAmount':takeAmount,
						'recivedAmount':recivedAmount
					}
					return render(request,'index.html',to_return)
				sale.save()
				return redirect('/index/' + str(sale.id))

		if request.POST['inputProduct'] == 'transactionDone':
			if done.is_valid():
				aux = done.save(commit=False)
				sale.done = aux.done
				sale.save()

	else:
		addProd = ProductBillForm()
		modifyProd = PBFormSet()
		searchBill = SearchBillForm()
		searchCli = SearchCliForm()
		takeAmount = InputMoney()
		recivedAmount = InputMoney()
		done = InputTrue()
	return render(request,'index.html',{'workerNow':workerNow,'oldProds':oldProds,'date':date, 'market':marketNow, 'sale':sale,'addProd':addProd,'fail':fail,'mixList':mixList,'searchBill':searchBill,'searchCli':searchCli,'takeAmount':takeAmount,'recivedAmount':recivedAmount})


def addToSale(newAdded,sale):
	price = Product.objects.get(pk=newAdded.product.pk)

	if price.amount >= newAdded.amount:
		price.amount = price.amount - newAdded.amount
		price.save()

		newAdded.sellPrice = price.sellPrice
		newAdded.totAmount = newAdded.sellPrice * newAdded.amount

		sale.subtotal = sale.subtotal + newAdded.totAmount
		sale.totAmount = sale.totAmount + newAdded.totAmount
		if sale.recivedAmount > 0:
			sale.devolution = sale.devolution + newAdded.totAmount
		sale.save()

		newAdded.sale=sale
		newAdded.save()
		return False #redirect('/index/' + str(sale.id))
	else:
		fail = "¡Error!: Quedan " + str(price.amount) + " " + str(price.product.kind)
		return fail

'''
@login_required(login_url='/')
def newProduct(request):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	if request.method == 'POST':
		newprovider = ProviderForm(request.POST)
		newrawprod = RawProductForm(request.POST)
		newprod = ProductForm(request.POST)
		if request.POST['inputInNewProd'] == 'newProvider':
			if newprovider.is_valid():
				provider = newprovider.save()
				return redirect('/new_product')
		if request.POST['inputInNewProd'] == 'newProd':
			if newrawprod.is_valid() * newprod.is_valid():
				#rawProd = newrawprod.save(commit=False)
				#rawProd.provider = provider
				rawProd = newrawprod.save()
				prod = newprod.save(commit=False)
				prod.product = rawProd
				prod.market = workerNow.market
				prod.save()
				return redirect('/new_product')
			else:
				print "¡Error!: No se han cumplimentado correctamente los datos del producto."
	else:
		newprovider = ProviderForm()
		newrawprod = RawProductForm()
		newprod = ProductForm()
	return render(request,'productForm.html',{'workerNow':workerNow,'newprovider':newprovider,'newrawprod':newrawprod,'newprod':newprod})
'''

@login_required(login_url='/')
def deleteItem(request,sale_id,item_id):
	sale = Sale.objects.get(id=sale_id)
	item = ProductBill.objects.get(id=item_id)
	product = Product.objects.get(id=item.product.id)
	product.amount = product.amount + item.amount
	product.save()
	sale.totAmount = sale.totAmount - item.totAmount
	sale.subtotal = sale.subtotal - item.totAmount
	if sale.recivedAmount > 0:
		sale.devolution = sale.devolution - item.totAmount
	sale.save()
	item.delete()
	return redirect('/index/' + sale_id)

@login_required(login_url='/')
def deleteSale(request,sale_id):
	sale = Sale.objects.get(id=sale_id)
	products = ProductBill.objects.filter(sale=sale)

	for i in products:
		'''
		prod = Product.objects.get(pk=i.product.pk)
		prod.amount = prod.amount + i.amount
		prod.save()
		'''
		deleteItem(request,str(sale.id),str(i.id))
		i.delete()
	deleteClient(request,str(sale.id))
	sale.delete()

	return redirect('/index')

@login_required(login_url='/')
def newClient(request):
	workerNow = Worker.objects.get(user=request.user)

	if request.method == 'POST':
		newClient = ClientForm(request.POST)
		if request.POST['inputInNewCli'] == 'newCli':
			if newClient.is_valid():
				auxCli = newClient.save(commit=False)
				auxCli.market = workerNow.market
				auxCli.save()
				return redirect('/clients')
	else:
		newClient = ClientForm()

	to_return = {
		'newClient':newClient,
		'workerNow':workerNow
	}

	return render(request,'addClient.html',to_return)

@login_required(login_url='/')
def deleteClient(request,sale_id):
	sale = Sale.objects.get(id = sale_id)
	if sale.usedWallet > 0.0:
		sale.totAmount = sale.totAmount + sale.usedWallet
		if sale.recivedAmount > 0:
			sale.devolution = sale.devolution + sale.usedWallet
		buyer = Client.objects.get(pk=sale.buyer.pk)
		buyer.wallet = buyer.wallet + sale.usedWallet
		sale.usedWallet = 0.0
		buyer.save()
	sale.buyer = None
	sale.save()
	return redirect('/index/' + sale_id)
'''
@login_required(login_url='/')
def listProducts(request):
	workerNow = Worker.objects.get(user=request.user)
	marketNow = workerNow.market
	products = Product.objects.filter(market=marketNow)
	fail = None

	if request.method == 'POST':
		searchProduct = SearchProduct(request.POST)
		#modifyAmount = AmountForm(request.POST)
		if request.POST['searching'] == 'searchProd':
			if searchProduct.is_valid():
				aux = searchProduct.save(commit=False)
				productsAux = RawProduct.objects.filter(name=aux)
				counter = 0
				listAux = []
				for i in productsAux:
					for j in products:
						if i == j.product:
							counter = 1
							listAux.append(j)
				if counter == 0:
					fail = "¡Error!: No se ha encontrado el producto."
				else:
					products = listAux

		#if request.POST['modAmount'] == 'newAmount':
		#	if modifyAmount.is_valid():
		#		aux = modifyAmount.save(commit=False)

	else:
		searchProduct = SearchProduct()

	to_return = {
		'workerNow':workerNow,
		'marketNow':marketNow,
		'products':products,
		'searchProduct':searchProduct,
		'fail':fail
	}

	return render(request,'productos.html',to_return)
'''
@login_required(login_url='/')
def deleteProduct(request,product_id):
	workerNow = Worker.objects.get(user=request.user)
	marketNow = workerNow.market
	product = Product.objects.get(id=product_id,market=marketNow)

	product.product.delete()
	product.delete()

	return redirect('/products')
'''
@login_required(login_url='/')
def modifyProduct(request,product_id):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	product = Product.objects.get(id=product_id)
	#print "PRODUCTOOOOO ",product.id
	if request.method == 'POST':
		newprovider = ProviderForm(request.POST)
		newrawprod = RawProductForm(request.POST,instance=product.product)
		newprod = ProductForm(request.POST,instance=product)
		if request.POST['inputInNewProd'] == 'newProvider':
			if newprovider.is_valid():
				provider = newprovider.save()
				return redirect('/modProd/' + product_id)
		if request.POST['inputInNewProd'] == 'newProd':
			if newrawprod.is_valid() * newprod.is_valid():
				rawProd = newrawprod.save()
				prod = newprod.save(commit=False)
				prod.product = rawProd
				prod.market = workerNow.market
				prod.save()
				return redirect('/products')
			else:
				print "¡Error!: No se han cumplimentado correctamente los datos del producto."
	else:
		newprovider = ProviderForm()
		newrawprod = RawProductForm(instance=product.product)
		newprod = ProductForm(instance=product)
	return render(request,'productForm.html',{'workerNow':workerNow,'newprovider':newprovider,'newrawprod':newrawprod,'newprod':newprod}, context_instance=RequestContext(request))
'''
@login_required(login_url='/')
def listClients(request):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	clients = Client.objects.filter(market=marketNow)
	fail = None

	if request.method == 'POST':
		searchClie = SrchCliForm(request.POST)
		if request.POST['searchCli'] == 'newSearch':
			if searchClie.is_valid():
				aux = searchClie.save(commit=False)
				listAux = []
				counter = 0
				for i in clients:
					if i.name == aux.name:
						counter = 1
						listAux.append(i)
				if counter == 0:
					fail = "¡Error!: No se han encontrado clientes con ese nombre."
				else:
					clients = listAux
	else:
		searchClie = SrchCliForm()


	to_return = {
		'workerNow':workerNow,
		'marketNow':marketNow,
		'clients':clients,
		'searchClie':searchClie,
		'fail':fail
	}
	return render(request,'clients.html',to_return)


@login_required(login_url='/')
def modClient(request,pk):
	workerNow = Worker.objects.get(user=request.user)
	client = Client.objects.get(pk=pk)

	if request.method == 'POST':
		newClient = ClientForm(request.POST,instance=client)
		if request.POST['inputInNewCli'] == 'newCli':
			if newClient.is_valid():
				auxCli = newClient.save(commit=False)
				auxCli.market = workerNow.market
				auxCli.save()
				return redirect('/clients')
	else:
		newClient = ClientForm(instance=client)

	to_return = {
		'newClient':newClient,
		'workerNow':workerNow
	}

	return render(request,'addClient.html',to_return)

@login_required(login_url='/')
def clientProfile(request,pk):
	userNow = request.user
	workerNow = Worker.objects.get(user=userNow)
	marketNow = workerNow.market
	client = Client.objects.get(pk=pk)
	sales = Sale.objects.filter(market=marketNow,buyer=client)

	to_return = {
		'workerNow':workerNow,
		'marketNow':marketNow,
		'client':client,
		'sales':sales
	}

	return render(request,'clientProfile.html',to_return)
