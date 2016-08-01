#encoding:utf-8
from django.forms import ModelForm
from django import forms
from TPVpnapp.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.extras.widgets import SelectDateWidget
from django.template.defaultfilters import mark_safe

class UserForm(UserCreationForm):
	username=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	email=forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	password1=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	password2=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	first_name=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	last_name=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	class Meta:
		model = User
		fields=('username','email','password1','password2','first_name','last_name')

class RegisterBusinessForm(ModelForm):
	name=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la tienda*'}), label='')
	kindActivity=forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'¿Que tipo de actividad realiza?'}), label='')
	secretKey=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña*'}), label='')
	secretKey2=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repita la contraseña*'}), label='')
	tel = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Teléfono*'}), label='')
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'E-mail*'}), label='')
	class Meta:
		model=Market
		fields=('name','tel','email','kindActivity','secretKey','secretKey2')

class RegisterFullDirectionForm(ModelForm):
	#id=forms.IntegerField(widget=forms.HiddenInput(),label='')
	location=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Localidad*'}), label='')
	province=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Provincia*'}), label='')
	postalCode=forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Código postal*'}), label='')
	direction=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección*'}), label='')
	numDir=forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número*'}), label='')
	stairs=forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escaleras'}), label='')
	numFlat=forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Planta'}), label='')
	door=forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Puerta'}), label='')
	class Meta:
		model=FullDirection
		fields=('location','province','postalCode','direction','numDir','stairs','numFlat','door')

class RegisterWorker(ModelForm):
	dni = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	genre = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'class':'form-control', 'name':'gender'}), choices=GENRE, label='')
	segSocial = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	tel1 = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	tel2 = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':''}), label='')
	image = forms.FileField(required=False, widget=forms.FileInput, label='')
	#market = forms.ModelChoiceField(required=True, queryset=Market.objects.all(), widget=forms.Select(attrs={'class':'form-control col-md-6 col-sm-6 col-xs-12'}), label='Escoja un comercio')
	#marketKey = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña del negocio*'}), label='')
	class Meta:
		model=Worker
		fields=('dni','genre','segSocial','tel1','tel2','image')

class PasswordMarketForm(ModelForm):
	secretKey = forms.CharField(
	required=True, widget=forms.PasswordInput(attrs = {
			'class':'form-control',
		}), label='')
	class Meta:
		model=Market
		fields = ('secretKey',)

#Formulario sin modelo
class SearchWorkerForm(forms.Form):
	array = forms.CharField(
	required=True, widget=forms.TextInput(attrs = {
			'class':'form-control',
			'placeholder':'Buscar...',
			'title':'Login, Nombre, Apellidos o DNI'
		}), label='')
	class Meta:
		fields = ('array',)

class SearchClientForm(forms.Form):
	array = forms.CharField(
	required=True, widget=forms.TextInput(attrs = {
			'class':'form-control',
			'placeholder':'Buscar...',
			'title':'Nombre, Apellidos, DNI o e-mail'
		}), label='')
	class Meta:
		fields = ('array',)

class NotificationForm(ModelForm):
	content = forms.CharField(
		required = True,
		widget=forms.Textarea(attrs = {
			'class':'form-control',
			'rows':'3',
			'style':'resize:none'
		}),
		label='')
	class Meta:
		model=Notification
		fields = ('content',)

class LoginForm(AuthenticationForm):
	username=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Login de usuario'}), label='')
	password=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}), label='')
	#class Meta:
	#	model=User
	#	fields=('username','password')
	def authentication(self,username,password):
		if User.objects.filter(username=username,password=password):
			return User.objects.get(username=username)

class ProviderForm(ModelForm): #REVISADO
	namePro = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}), label='')
	tel = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control col-md-7 col-xs-12'}), label='')
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}), label='')
	class Meta:
		model = Provider
		fields = ('namePro','tel','email')

class ProductForm(ModelForm): #REVISADO
	provider = forms.ModelChoiceField(
		required=True, queryset=Provider.objects.all(),
		widget=forms.Select(attrs={
			'class':'select2_single form-control col-md-7 col-xs-12'
		}),
		label=''
	)
	name = forms.CharField(
		required=True,
		widget=forms.TextInput(attrs = {
				'class':'form-control col-md-7 col-xs-12'
		}),
		label=''
	)
	category = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}), label='')
	subcategory = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}), label='')
	brand = forms.CharField(
		required=True,
		widget=forms.TextInput(attrs={
			'class':'form-control col-md-7 col-xs-12'
		}),
		label=''
	)
	buyPrice = forms.FloatField(
		required=True,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control col-md-7 col-xs-12',
				'placeholder':'Ej: 5,50'
			}
		),
		label=''
	)
	kind = forms.ChoiceField(required=True, choices = KINDPRODUCT, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12'}) ,label = '' )
	iva = forms.ChoiceField(
		required=True, choices = IVA,
		widget=forms.Select(attrs = {
			'class':'form-control'
		}) ,label='' )
	amount = forms.FloatField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control col-md-7 col-xs-12',
				'placeholder':'Ej: 10,3'
			}),
		label = ''
	)
	sellPrice = forms.FloatField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control col-md-7 col-xs-12',
				'placeholder':'Ej: 5,50'
			}
		),
		label=''
	)
	barCode = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}), label='')
	image = forms.ImageField(required=False, widget=forms.FileInput, label='')
	class Meta:
		model = Product
		fields = (
			'name','provider','category','subcategory','brand',
			'buyPrice','sellPrice','amount','kind','iva','barCode','image'
		)

class StockForm(forms.Form):
	new = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs = {
				'class':'form-control col-md-7 col-xs-12',
				'placeholder':'',
				'title':''
			}
		),
		label=''
	)
	add = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs = {
				'class':'form-control col-md-7 col-xs-12',
				'placeholder':'Ejemplo: 1, -5, 1.5, etc.',
				'title':''
			}
		),
		label=''
	)
	class Meta:
		fields = ('new','add')

class OfferForm(forms.Form):
	offer = forms.FloatField(
		required = False,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		),
		label = ''
	)
	class Meta:
		fields = ('offer',)

class ClientForm(ModelForm):  #REVISADO
	name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12','placeholder':'Nombre Completo'}), label='')
	dni = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12','placeholder':'DNI'}), label='')
	tel = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12','placeholder':'Teléfono'}), label='')
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12','placeholder':'E-mail'}), label='')
	wallet = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12','placeholder':'Cuantía'}), label='',initial='0.0')
	image = forms.FileField(required=False, widget=forms.FileInput, label='')
	class Meta:
		model = Client
		fields = ('name','dni','tel','email','wallet','image')

class InputMoney(forms.Form):
	new = forms.FloatField(
		required = False,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		),
		label = '',
		initial = 0.0
	)
	add = forms.FloatField(
		required = False,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		),
		label = '',
		initial = 0.0
	)
	class Meta:
		model = Client
		fields = ('new','add')


class InputTrue(ModelForm):
	done = forms.BooleanField(required=True,label='')
	class Meta:
		model = Sale
		fields = ('done',)

class SearchProduct(forms.Form):
	search = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control',
				'placeholder':'Buscar...',
				'title':'Nombre, Marca, Proveedor, Categoría o Código de Barras'
			}
		),
		label='')
	class Meta:
		fields = ('search',)


class AmountForm(ModelForm):
	amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control col-md-7 col-xs-12'}),label='')
	class Meta:
		model = Product
		fields = ('amount',)

class SrchCliForm(ModelForm):
	name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Buscar...'}), label='')
	class Meta:
		model = Client
		fields = ('name',)
