# encoding:utf-8

from django.contrib.auth.models import User
from django.db import models


class FullDirection(models.Model):
    location = models.CharField(max_length=100, blank=False, null=False)
    province = models.CharField(max_length=100, blank=False, null=False)
    postalCode = models.CharField(max_length=5, blank=False, null=False)
    direction = models.CharField(max_length=100, blank=False, null=False)
    numDir = models.CharField(max_length=4, blank=False, default='S/N')
    stairs = models.CharField(max_length=20, blank=True, null=True, default='')
    numFlat = models.IntegerField(blank=True, null=True)
    door = models.CharField(max_length=20, blank=True, null=True, default='')

    def __unicode__(self):
        return unicode(self.pk)


class Market(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    kindActivity = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    direction = models.ForeignKey(
        FullDirection, unique=False, null=True, blank=True
    )
    # secretKey = models.CharField(max_length=16, blank=False, null=False)
    # secretKey2 = models.CharField(max_length=16, blank=False, null=False)
    tel = models.IntegerField()
    email = models.EmailField()

    def __unicode__(self):
        return unicode(self.name)


class Provider(models.Model):
    market = models.ForeignKey(Market, blank=False, null=False, default=None)
    namePro = models.CharField(max_length=100)
    tel = models.IntegerField()
    email = models.EmailField()

    def __unicode__(self):
        return unicode(self.namePro)


class Offer(models.Model):
    offer = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return unicode(self.pk)

KINDPRODUCT = (
    ('Unidades', 'Unidades'),
    ('Kilos', 'Kilos'),
    ('Gramos', 'Gramos')
)

IVA = (
    ('', 'IVA'),
    (21, '21%'),
    (10, '10%'),
    (4, '4%'),
)


class Product(models.Model):
    name = models.CharField(max_length=120, blank=False)
    provider = models.ForeignKey(Provider)
    category = models.CharField(max_length=120, blank=False, default='Ninguna')
    subcategory = models.CharField(max_length=120, blank=False,
                                   default='Ninguna')
    brand = models.CharField(
        max_length=120, blank=False, null=False, default='Blanca'
    )
    buyPrice = models.FloatField(max_length=10, blank=True, null=True)
    sellPrice = models.FloatField(max_length=10, blank=False, null=False)
    offer = models.ForeignKey(Offer, blank=True, null=True)
    amount = models.FloatField(max_length=10, blank=True, null=True)
    kind = models.CharField(
        max_length=20, blank=False, null=False,
        choices=KINDPRODUCT, default='Unidades'
    )
    iva = models.IntegerField(blank=False, choices=IVA, default=21)
    # Relacion 1:N - Mercado puede tener muchos productos
    market = models.ForeignKey(Market, related_name='market')
    barCode = models.CharField(max_length=120, blank=True, null=True,
                               default='Vacio')
    image = models.ImageField(
        blank=True, null=True, upload_to='products/uploaded',
        default='products/default/product.png'
    )

    def __unicode__(self):
        return unicode(self.name)

GENRE = (
    ('', '------'),
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
)


class Worker(models.Model):
    user = models.OneToOneField(User, unique=True, default=None)
    # Relacion 1:N - Mercado puede tener muchos trabajadores
    market = models.ForeignKey(Market, null=True, blank=True)
    dni = models.CharField(max_length=9)
    genre = models.CharField(max_length=20, choices=GENRE)
    segSocial = models.CharField(max_length=12)
    tel1 = models.IntegerField(blank=False, null=False)
    tel2 = models.IntegerField(blank=True, null=True)
    home = models.ForeignKey(FullDirection, null=True, blank=True)
    image = models.ImageField(blank=False, null=False,
                              upload_to='users/profile',
                              default='users/default/img.jpg')

    class Meta:
        unique_together = (("market", "dni"), ("market", "segSocial"), )

    def __unicode__(self):
        return unicode(self.user.username)

    def get_full_name(self):
        return unicode(self.user.first_name + ' ' + self.user.last_name)


class Client(models.Model):
    name = models.CharField(max_length=120)
    # Relacion 1:N - Mercado puede tener muchos clientes
    market = models.ForeignKey(Market)
    image = models.ImageField(blank=True, null=True,
                              default='clients/default/img.jpg',
                              upload_to='clients/profile')
    dni = models.CharField(max_length=9)
    email = models.EmailField(blank=True, null=True, default=None)
    tel = models.IntegerField(blank=True, null=True, default=None)
    wallet = models.FloatField(blank=False, null=False, default=0.0)

    class Meta:
        unique_together = (("market", "dni"), )

    def __unicode__(self):
        return unicode(self.name)


class Sale(models.Model):
    sale_code = models.CharField(max_length=1000000, default=None, blank=True,
                                 null=True)
    # Relacion 1:N - Mercado puede tener muchas ventas
    market = models.ForeignKey(Market)
    # Relacion 1:N - Trabajador puede tener muchas ventas
    seller = models.ForeignKey(Worker)
    # Relacion 1:N - Cliente puede tener muchas compras
    buyer = models.ForeignKey(Client, blank=True, null=True, default=None)
    # CAMPO INNECESARIO?
    # subtotal = models.FloatField(max_length=100, default=0.0)
    totAmount = models.FloatField(max_length=100, blank=True, default=0.0)
    usedWallet = models.FloatField(max_length=100, blank=True, default=0.0)
    recivedAmount = models.FloatField(max_length=100, blank=True, default=0.0)
    devolution = models.FloatField(max_length=100, blank=True, default=0.0)
    benefice = models.FloatField(blank=True, null=True, default=0.0)
    done = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.pk)


class ProductSale(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    # Relacion 1:N - Venta puede tener muchos productos
    sale = models.ForeignKey(Sale, default=None)
    amount = models.FloatField(max_length=10, blank=False, default=1.0)
    sellPrice = models.FloatField(blank=True, null=True)
    totAmount = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.pk)

TYPENOTE = (
    ('normal', 'normal'),
    ('wallet', 'wallet'),
)


class Notification(models.Model):
    reciver = models.ForeignKey(Worker, default=None, blank=True, null=True,
                                related_name='reciver')
    reciverCli = models.ForeignKey(Client, default=None, blank=True, null=True)
    writer = models.ForeignKey(Worker, default=None, blank=True, null=True,
                               related_name='writer')
    content = models.CharField(max_length=500, blank=False, null=False)
    typeNote = models.CharField(max_length=20, choices=TYPENOTE)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.pk)


class Configuration(models.Model):
    worker = models.OneToOneField(Worker)
    stock_enabled = models.BooleanField(default=True)
    max_negative_wallet = models.FloatField(
        blank=True, null=True,
        verbose_name='¿Valor tope minimo del monedero?'
    )

    def __unicode__(self):
        return self.worker.get_full_name()
