from django.contrib import admin

# Register your models here.
from TPVpnapp.models import (Client, FullDirection, Market, Notification,
                             Product, ProductSale, Provider, Sale, Worker,
                             Offer)

admin.site.register(FullDirection)
admin.site.register(Market)
admin.site.register(Provider)
admin.site.register(Product)
admin.site.register(Worker)
admin.site.register(Sale)
admin.site.register(ProductSale)
admin.site.register(Client)
admin.site.register(Notification)
admin.site.register(Offer)
