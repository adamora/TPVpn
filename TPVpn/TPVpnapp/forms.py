# encoding:utf-8
from datetime import datetime

from TPVpnapp.models import (Client, FullDirection, GENRE, IVA, KINDPRODUCT,
                             Market, Notification, Product, Provider, User,
                             Worker, Sale)

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.utils.dateparse import parse_date


class UserForm(UserCreationForm):
    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                      'placeholder': ''}))
    email = forms.EmailField(required=True, label='',
                             widget=forms.EmailInput(attrs={
                                                     'class': 'form-control',
                                                     'placeholder': ''}))
    password1 = forms.CharField(required=True, label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': ''}))
    password2 = forms.CharField(required=True, label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': ''}))
    first_name = forms.CharField(required=True, label='',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': ''}))
    last_name = forms.CharField(required=True, label='',
                                widget=forms.TextInput(attrs={
                                                       'class': 'form-control',
                                                       'placeholder': ''}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name',
                  'last_name')


class RegisterBusinessForm(ModelForm):
    name = forms.CharField(required=True, label='',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Nombre de la tienda*'}))
    kindActivity = forms.CharField(required=False, label='',
                                   widget=forms.Textarea(
                                       attrs={'class': 'form-control',
                                              'placeholder':
                                              '¿Que tipo de actividad realiza?'
                                              }))
    secretKey = forms.CharField(required=True, label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Contraseña*'}))
    secretKey2 = forms.CharField(required=True, label='',
                                 widget=forms.PasswordInput(
                                     attrs={'class': 'form-control',
                                            'placeholder':
                                            'Repita la contraseña*'}))
    tel = forms.IntegerField(required=True, label='',
                             widget=forms.NumberInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'Teléfono*'}))
    email = forms.EmailField(required=True, label='',
                             widget=forms.EmailInput(attrs={
                                                     'class': 'form-control',
                                                     'placeholder': 'E-mail*'
                                                     }))

    class Meta:
        model = Market
        fields = ('name', 'tel', 'email', 'kindActivity', 'secretKey',
                  'secretKey2')


class FullDirectionForm(ModelForm):
    # id=forms.IntegerField(widget=forms.HiddenInput(),label='')
    location = forms.CharField(required=True, label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Localidad*'}))
    province = forms.CharField(required=True, label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Provincia*'}))
    postalCode = forms.IntegerField(required=True, label='',
                                    widget=forms.NumberInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Código postal*'
                                               }))
    direction = forms.CharField(required=True, label='',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Dirección*'}))
    numDir = forms.CharField(required=False, label='',
                             widget=forms.TextInput(attrs={
                                                    'class': 'form-control',
                                                    'placeholder': 'Número*'}))
    stairs = forms.CharField(required=False, label='',
                             widget=forms.TextInput(attrs={
                                                    'class': 'form-control',
                                                    'placeholder': 'Escaleras'
                                                    }))
    numFlat = forms.IntegerField(required=False, label='',
                                 widget=forms.NumberInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Planta'}))
    door = forms.CharField(required=False, label='',
                           widget=forms.TextInput(attrs={
                                                  'class': 'form-control',
                                                  'placeholder': 'Puerta'}))

    class Meta:
        model = FullDirection
        fields = ('location', 'province', 'postalCode', 'direction', 'numDir',
                  'stairs', 'numFlat', 'door')


class RegisterWorker(ModelForm):
    dni = forms.CharField(required=True, label='',
                          widget=forms.TextInput(attrs={
                                                 'class': 'form-control',
                                                 'placeholder': ''}))
    genre = forms.ChoiceField(required=False, choices=GENRE, label='',
                              widget=forms.RadioSelect(attrs={
                                                       'class': 'form-control',
                                                       'name': 'gender'}))
    segSocial = forms.CharField(required=True, label='',
                                widget=forms.TextInput(attrs={
                                                       'class': 'form-control',
                                                       'placeholder': ''}))
    tel1 = forms.IntegerField(required=True, label='',
                              widget=forms.NumberInput(attrs={
                                                       'class': 'form-control',
                                                       'placeholder': ''}))
    tel2 = forms.IntegerField(required=False, label='',
                              widget=forms.NumberInput(
                                  attrs={'class': 'form-control',
                                         'placeholder': ''}))
    image = forms.FileField(required=False, widget=forms.FileInput, label='')

    class Meta:
        model = Worker
        fields = ('dni', 'genre', 'segSocial', 'tel1', 'tel2', 'image')


class PasswordMarketForm(ModelForm):
    secretKey = forms.CharField(required=True, label='',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control'
                                    }))

    class Meta:
        model = Market
        fields = ('secretKey',)


class SearchWorkerForm(forms.Form):
    array = forms.CharField(required=True, label='',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Buscar...',
                                'title': 'Login, Nombre, Apellidos o DNI'}))

    class Meta:
        fields = ('array',)


class SearchClientForm(forms.Form):
    array = forms.CharField(required=True, label='',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Buscar...',
                                       'title':
                                       'Nombre, Apellidos, DNI o e-mail'}))

    class Meta:
        fields = ('array',)


class NotificationForm(ModelForm):
    content = forms.CharField(required=True, label='',
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control',
                                         'rows': '3',
                                         'style': 'resize:none'}))

    class Meta:
        model = Notification
        fields = ('content',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Login de usuario'}))
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Contraseña'}))

    def authentication(self, username, password):
        if User.objects.filter(username=username, password=password):
            return User.objects.get(username=username)


class ProviderForm(ModelForm):
    namePro = forms.CharField(required=True, label='',
                              widget=forms.TextInput(
                                  attrs={'class':
                                         'form-control col-md-7 col-xs-12'}))
    tel = forms.IntegerField(required=True, label='',
                             widget=forms.NumberInput(
                                 attrs={'class':
                                        'form-control col-md-7 col-xs-12'}))
    email = forms.EmailField(required=True, label='',
                             widget=forms.EmailInput(
                                 attrs={'class':
                                        'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Provider
        fields = ('namePro', 'tel', 'email')


class ProductForm(ModelForm):
    provider = forms.ModelChoiceField(required=True, label='',
                                      queryset=Provider.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class':
                                                 'select2_single form-control'
                                                 'col-md-7 col-xs-12'}))
    name = forms.CharField(required=True, label='',
                           widget=forms.TextInput(
                               attrs={'class':
                                      'form-control col-md-7 col-xs-12'}))
    category = forms.CharField(required=False, label='',
                               widget=forms.TextInput(
                                   attrs={'class':
                                          'form-control col-md-7 col-xs-12'}))
    subcategory = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'class':
                                             'form-control col-md-7 col-xs-12'}
                                  ), label='')
    brand = forms.CharField(required=True, label='',
                            widget=forms.TextInput(
                                attrs={'class':
                                       'form-control col-md-7 col-xs-12'}))
    buyPrice = forms.FloatField(required=True, label='',
                                widget=forms.TextInput(
                                    attrs={'class':
                                           'form-control col-md-7 col-xs-12',
                                           'placeholder': 'Ej: 5,50'}))
    kind = forms.ChoiceField(required=True, choices=KINDPRODUCT, label='',
                             widget=forms.Select(
                                 attrs={'class':
                                        'form-control col-md-7 col-xs-12'}))
    iva = forms.ChoiceField(required=True, choices=IVA, label='',
                            widget=forms.Select(attrs={
                                'class': 'form-control'}))
    amount = forms.FloatField(required=True, label='',
                              widget=forms.TextInput(
                                  attrs={'class':
                                         'form-control col-md-7 col-xs-12',
                                         'placeholder': 'Ej: 10,3'}))
    sellPrice = forms.FloatField(required=True, label='',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Ej: 5,50',
                                            'class':
                                            'form-control col-md-7 col-xs-12'
                                            }))
    barCode = forms.CharField(required=False, label='',
                              widget=forms.TextInput(
                                  attrs={
                                      'class':
                                      'form-control col-md-7 col-xs-12'}))
    image = forms.ImageField(required=False, widget=forms.FileInput, label='')

    class Meta:
        model = Product
        fields = ('name', 'provider', 'category', 'subcategory', 'brand',
                  'buyPrice', 'sellPrice', 'amount', 'kind', 'iva', 'barCode',
                  'image')


class StockForm(forms.Form):
    new = forms.CharField(required=False, label='',
                          widget=forms.TextInput(
                              attrs={'placeholder': '', 'title': '', 'class':
                                     'form-control col-md-7 col-xs-12'}))
    add = forms.CharField(required=False, label='',
                          widget=forms.TextInput(
                              attrs={'class':
                                     'form-control col-md-7 col-xs-12',
                                     'placeholder':
                                     'Ejemplo: 1, -5, 1.5, etc.',
                                     'title': ''}))

    class Meta:
        fields = ('new', 'add')


class ClientForm(ModelForm):
    name = forms.CharField(required=True, label='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Nombre Completo',
                                      'class':
                                      'form-control col-md-7 col-xs-12'}))
    dni = forms.CharField(required=True,
                          widget=forms.TextInput(
                              attrs={'class':
                                     'form-control col-md-7 col-xs-12',
                                     'placeholder': 'DNI'}), label='')
    tel = forms.IntegerField(required=False,
                             widget=forms.TextInput(
                                 attrs={'class':
                                        'form-control col-md-7 col-xs-12',
                                        'placeholder': 'Teléfono'}), label='')
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(
                                 attrs={'class':
                                        'form-control col-md-7 col-xs-12',
                                        'placeholder': 'E-mail'}), label='')
    wallet = forms.FloatField(required=True, label='', initial='0.0',
                              widget=forms.TextInput(
                                  attrs={'class':
                                         'form-control col-md-7 col-xs-12',
                                         'placeholder': 'Cuantía'}))
    image = forms.FileField(required=False, label='', widget=forms.FileInput)

    class Meta:
        model = Client
        fields = ('name', 'dni', 'tel', 'email', 'wallet', 'image')


class InputMoney(forms.Form):
    new = forms.FloatField(required=False, label='', initial=0.0,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    add = forms.FloatField(required=False, label='', initial=0.0,
                           widget=forms.TextInput(attrs={'class':
                                                         'form-control'}))

    class Meta:
        model = Client
        fields = ('new', 'add')


class SearchProduct(forms.Form):
    search = forms.CharField(required=True, label='',
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Buscar...',
                                     'title':
                                     'Nombre, Marca, Proveedor, Categoría o '
                                     'Código de Barras'}))

    class Meta:
        fields = ('search',)


class DateForm(forms.Form):
    start_date = forms.CharField(required=False, label='Fecha Inicio')
    end_date = forms.CharField(required=False, label='Fecha Fin')

    def __init__(self, categorys=None, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        # self.fields['start_date'].widget = extras.SelectDateWidget()
        self.fields['start_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'datepicker',
            'placeholder': 'Fecha inicio'
        }
        # self.fields['end_date'].widget = extras.SelectDateWidget()
        self.fields['end_date'].widget.attrs = {'class': 'form-control',
                                                'id': 'datepicker_2',
                                                'placeholder': 'Fecha fin'}
        if categorys:
            self.fields['categorys'] = forms.ChoiceField(required=False,
                                                         label='Categorías',
                                                         choices=categorys)
            self.fields['categorys'].widget.attrs = {
                'class': 'select2_single_category form-control'
            }

    def get_filter(self, market):
        objects = self.cleaned_data
        first_d = Sale.objects.first().date
        last_d = Sale.objects.last().date

        for field_name, val in objects.items():
            if not val:
                del self.cleaned_data[field_name]
            else:
                if field_name == 'start_date':
                    val = '-'.join(reversed(val.split('/')))
                    start_date = parse_date(val)
                    first_d = datetime.combine(start_date, datetime.min.time())
                    del self.cleaned_data[field_name]
                elif field_name == 'end_date':
                    val = '-'.join(reversed(val.split('/')))
                    end_date = parse_date(val)
                    last_d = datetime.combine(end_date, datetime.max.time())
                    del self.cleaned_data[field_name]
                elif field_name == 'categorys':
                    products_query = Product.objects.filter(category=val)
                    big_list = set([])
                    for i in products_query:
                        for j in i.productsale_set.all():
                            big_list.add(j.sale.id)
                    self.cleaned_data['id__in'] = big_list
                    del self.cleaned_data[field_name]
        self.cleaned_data['date__range'] = (first_d, last_d)
        return self.cleaned_data
