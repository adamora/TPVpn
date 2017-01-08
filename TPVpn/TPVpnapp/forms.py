# encoding:utf-8
from datetime import datetime

from TPVpnapp.models import (Client, Configuration, FullDirection, GENRE, IVA,
                             KINDPRODUCT, Market, Notification, Product,
                             Provider, User, Worker, Sale, Offer)

from django import forms
from django.contrib import messages
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

    def __init__(self, is_mod=False, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if is_mod:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields.pop('password1')
            self.fields.pop('password2')
        else:
            self.fields['password1'].widget.attrs = {
                'class': 'form-control',
                'placeholder': ''}
            self.fields['password2'].widget.attrs = {
                'class': 'form-control',
                'placeholder': ''}

    def is_valid(self, request):
        is_valid = super(UserForm, self).is_valid()
        if not is_valid:
            if self.errors:
                for key, value in self.errors.items():
                    if isinstance(value, list):
                        msg = key + ': ' + value[0]
                    else:
                        msg = key + ': ' + value
                    messages.warning(request, msg)
            if self.error_messages:
                for key, value in self.error_messages.items():
                    if isinstance(value, list):
                        msg = key + ': ' + value[0].title()
                    else:
                        msg = key + ': ' + value.title()
                    messages.warning(request, msg)
        return is_valid


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
        fields = ('name', 'tel', 'email', 'kindActivity')


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
    numDir = forms.CharField(
        required=False, label='',
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
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
    dni = forms.CharField(required=True, label='DNI',
                          widget=forms.TextInput(attrs={
                                                 'class': 'form-control',
                                                 'placeholder': ''}))
    genre = forms.ChoiceField(required=True, choices=GENRE, label='Género',
                              widget=forms.RadioSelect(attrs={
                                                       'class': 'form-control',
                                                       'name': 'gender'}))
    segSocial = forms.CharField(required=True, label='Seguridad Social',
                                widget=forms.TextInput(attrs={
                                                       'class': 'form-control',
                                                       'placeholder': ''}))
    tel1 = forms.IntegerField(required=True, label='Teléfono',
                              widget=forms.NumberInput(attrs={
                                                       'class': 'form-control',
                                                       'step': '1'}))
    tel2 = forms.IntegerField(required=False, label='Teléfono (Opcional)',
                              widget=forms.NumberInput(
                                  attrs={'class': 'form-control',
                                         'step': '1'}))
    image = forms.FileField(required=False, widget=forms.FileInput,
                            label='Imagen')

    class Meta:
        model = Worker
        fields = ('dni', 'genre', 'segSocial', 'tel1', 'tel2', 'image')

    def __init__(self, *args, **kwargs):
        super(RegisterWorker, self).__init__(*args, **kwargs)
        if 'instance' in kwargs.keys():
            self.fields['genre'].initial = self.instance.genre

    def is_valid(self, request):
        super(RegisterWorker, self).is_valid()
        if self.errors:
            for key, value in self.errors.items():
                if isinstance(value, list):
                    msg = key + ': ' + value[0]
                else:
                    msg = key + ': ' + value
                messages.error(request, msg)
            return False
        else:
            return True


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

    def is_valid(self, request):
        is_valid = super(NotificationForm, self).is_valid()
        if not is_valid:
            messages.warning(request,
                             'Rellene el campo de Mensaje para notificar.')
        return is_valid


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
                                      queryset=Provider.objects.all())
    name = forms.CharField(
        required=True, label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    category = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Crear nueva categoría'}
        )
    )
    subcategory = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Crear nueva subcategoría'}
        )
    )
    brand = forms.CharField(
        required=True, label='',
        widget=forms.TextInput(
            attrs={'class':
                   'form-control'}))
    buyPrice = forms.FloatField(
        required=True, label='',
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'step': "0.01",
                   'placeholder': "Usar ',' en decimales. Ej.: 11,5"}))
    kind = forms.ChoiceField(required=True, choices=KINDPRODUCT, label='',
                             widget=forms.Select(
                                 attrs={'class':
                                        'form-control col-md-7 col-xs-12'}))
    iva = forms.ChoiceField(required=True, choices=IVA, label='',
                            widget=forms.Select(attrs={
                                'class': 'form-control'}))
    amount = forms.FloatField(
        required=True, label='',
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'step': "0.001",
                   'placeholder': "Usar ',' en decimales. Ej.: 11,5"}))
    sellPrice = forms.FloatField(
        required=True, label='',
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'step': "0.01",
                   'placeholder': "Usar ',' en decimales. Ej.: 11,5"}))
    barCode = forms.CharField(required=False, label='',
                              widget=forms.TextInput(
                                  attrs={
                                      'class':
                                      'form-control col-md-7 col-xs-12'}))
    image = forms.ImageField(
        required=False, label='',
        widget=forms.FileInput(attrs={'hide': ''}))

    class Meta:
        model = Product
        fields = ('name', 'provider', 'category', 'subcategory', 'brand',
                  'buyPrice', 'sellPrice', 'amount', 'kind', 'iva', 'barCode',
                  'image')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['provider'].widget.attrs = {
            'class': 'select2_single_provider form-control',
        }


class GenericTwoRowsForm(forms.Form):
    new = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(
            attrs={'type': 'number',
                   'class': 'form-control',
                   'step': "0.01",
                   'placeholder': "Usar ',' en decimales. Ej.: 11,5"}))
    add = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(
            attrs={'type': 'number',
                   'class': 'form-control',
                   'step': "0.01",
                   'placeholder': "Usar ',' en decimales. Ej.: 11,5"}))


class StockForm(GenericTwoRowsForm):

    class Meta:
        fields = ('new', 'add')

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['new'].widget.attrs['step'] = '0.001'
        self.fields['add'].widget.attrs['step'] = '0.001'

    def is_valid(self, request, instance_prod):
        if super(StockForm, self).is_valid():
            cleaned_data = self.cleaned_data
            try:
                data = [float(i) for i in cleaned_data.values() if i]
            except:
                messages.error(request,
                               ("El formato de los campos " +
                                "introducidos no es correcto. " +
                                "Solo valores numéricos."))
                return False
            if data:
                if len(data) > 1:
                    messages.error(
                        request,
                        ("Ha rellenado los dos campos de Stock " +
                         "en el producto '%(prod)s'" %
                         {'prod': instance_prod.name}))
                    return False
            else:
                return False
            return True
        else:
            return False


class ClientForm(ModelForm):
    name = forms.CharField(required=True, label='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Nombre Completo',
                                      'class': 'form-control'}))
    dni = forms.CharField(required=True,
                          widget=forms.TextInput(
                              attrs={'class': 'form-control',
                                     'placeholder': 'DNI'}), label='')
    tel = forms.IntegerField(required=False,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'Teléfono',
                                        'type': 'tel'}), label='')
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'E-mail'}), label='')
    wallet = forms.FloatField(
        required=True, label='',
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'placeholder': "Cuantía. Usar ',' en decimales. Ej.: 11,5"})
    )
    image = forms.FileField(required=False, label='', widget=forms.FileInput)

    class Meta:
        model = Client
        fields = ('name', 'dni', 'tel', 'email', 'wallet', 'image')


class InputMoney(GenericTwoRowsForm):
    class Meta:
        exclude = []

    def is_valid(self, request):
        is_valid = super(InputMoney, self).is_valid()
        if is_valid:
            len_values = len([i for i in self.cleaned_data.values() if i])
            if len_values == 1:
                return True
            elif len_values > 1:
                messages.error(
                    request,
                    'Solo puede rellenar un campo en los valores de Monedero.')
            elif len_values < 1:
                messages.warning(
                    request,
                    'Rellene al menos un campo del Monedero editado.')
        else:
            messages.error(request, 'Datos de Monedero invalidos.')
        return False


class SearchProduct(forms.Form):
    search = forms.CharField(required=True, label='',
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Buscar por nombre...',
                                     'title':
                                     'Nombre, Marca, Proveedor, Categoría o '
                                     'Código de Barras'}))

    class Meta:
        fields = ('search',)

    def get_filter(self):
        my_filter = {}
        cleaned_data = self.cleaned_data
        for key, value in cleaned_data.items():
            if key == 'search' and value:
                my_filter.update({'name__icontains': value})
        return my_filter


class DateForm(forms.Form):
    start_date = forms.CharField(required=False, label='Fecha Inicio')
    end_date = forms.CharField(required=False, label='Fecha Fin')
    categorys = forms.ChoiceField(required=False, label='Categoría')

    def __init__(self, categorys, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        # self.fields['start_date'].widget = extras.SelectDateWidget()
        self.fields['start_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'datepicker',
            'placeholder': 'Fecha inicio'
        }
        # self.fields['end_date'].widget = extras.SelectDateWidget()
        self.fields['end_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'datepicker_2',
            'placeholder': 'Fecha fin'
        }
        self.fields['categorys'].widget = forms.Select(
            attrs={'class': 'select2_single_categorias form-control'})
        self.fields['categorys'].choices = categorys

    def get_filter(self, market):
        objects = self.cleaned_data
        first_d = Sale.objects.first().date
        last_d = Sale.objects.last().date
        big_list = None
        big_list_two = None

        for field_name, val in objects.items():
            if not val:
                del self.cleaned_data[field_name]
            else:
                if field_name == 'start_date':
                    val = '-'.join(reversed(val.split('/')))
                    start_date = parse_date(val)
                    first_d = datetime.combine(start_date, datetime.min.time())
                elif field_name == 'end_date':
                    val = '-'.join(reversed(val.split('/')))
                    end_date = parse_date(val)
                    last_d = datetime.combine(end_date, datetime.max.time())
                elif field_name == 'categorys':
                    products_query = Product.objects.filter(category=val,
                                                            market=market)
                    big_list = set([])
                    for i in products_query:
                        for j in i.productsale_set.all():
                            big_list.add(j.sale.id)
                    if big_list_two:
                        big_list = big_list.intersection(big_list_two)
                    self.cleaned_data['id__in'] = big_list
                elif field_name == 'iva':
                    products_query = Product.objects.filter(market=market,
                                                            iva=val)
                    big_list_two = set([])
                    for i in products_query:
                        for j in i.productsale_set.all():
                            big_list_two.add(j.sale.id)
                    if big_list:
                        big_list = big_list.intersection(big_list_two)
                    else:
                        big_list = big_list_two
                    self.cleaned_data['id__in'] = big_list
                del self.cleaned_data[field_name]
        self.cleaned_data['date__range'] = (first_d, last_d)
        return self.cleaned_data


class ConfigurationForm(forms.ModelForm):

    class Meta:
        model = Configuration
        exclude = ('worker', )

    def __init__(self, worker_now=None, *args, **kwargs):
        super(ConfigurationForm, self).__init__(*args, **kwargs)
        self.fields['max_negative_wallet'].initial = 0.0

    def clean_stock_enabled(self):
        val = self.cleaned_data.get('stock_enabled', None)
        if not val:
            self.cleaned_data['stock_enabled'] = False
        else:
            self.cleaned_data['stock_enabled'] = True

        return self.cleaned_data['stock_enabled']

    def clean_max_negative_wallet(self):
        val = self.cleaned_data.get('max_negative_wallet', None)
        if not val:
            self.cleaned_data['max_negative_wallet'] = None
        else:
            self.cleaned_data['max_negative_wallet'] = float(val)

        return self.cleaned_data['max_negative_wallet']

    def full_save(self, worker_now):
        instance = self.save(commit=False)
        instance.worker = worker_now
        instance.save()

        return instance


class ProductFilterForm(forms.Form):
    bar_code = forms.CharField(required=False, label='Código de barras')
    provider = forms.CharField(required=False, label='Proveedor')
    brand = forms.CharField(required=False, label='Marca')
    iva = forms.ChoiceField(required=False, label='IVA', choices=IVA,
                            initial='')

    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        self.fields['bar_code'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Código de Barras'}
        self.fields['provider'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Proveedor'}
        self.fields['brand'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Marca'}
        self.fields['iva'].widget.attrs = {
            'class': 'select2_single_iva form-control'
        }

    def get_filter(self):
        for key, value in self.cleaned_data.items():
            del self.cleaned_data[key]
            if value:
                if key == 'bar_code':
                    self.cleaned_data.update(
                        {'barCode__icontains': value})
                elif key == 'provider':
                    self.cleaned_data.update(
                        {'provider__namePro__icontains': value})
                elif key == 'brand':
                    self.cleaned_data.update({'brand__icontains': value})
                elif key == 'iva':
                    self.cleaned_data.update({'iva': value})
        return self.cleaned_data


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = []

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['offer'].widget.attrs = {
            'class': 'form-control',
            'step': "0.01",
            'placeholder': "Usar ',' en decimales. Ej.: 11,5"}
        self.fields['start_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'datepicker'}
        self.fields['end_date'].widget.attrs = {
            'class': 'form-control',
            'id': 'datepicker_2'}

    def is_valid(self, request):
        is_true = super(OfferForm, self).is_valid()
        if is_true:
            cleaned_data = self.cleaned_data
            if cleaned_data['start_date'] <= cleaned_data['end_date']:
                return True
            else:
                messages.error(request,
                               ('La fecha de fin de la oferta debe ' +
                                'ser mayor o igual a la fecha inicial'))
                return False
        else:
            if self.cleaned_data:
                messages.error(request, 'Oferta erronea')
            return is_true
