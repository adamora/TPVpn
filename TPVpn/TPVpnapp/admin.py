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


from django.contrib import admin

# Register your models here.
from TPVpnapp.models import (Client, FullDirection, Market, Notification,
                             Product, ProductSale, Provider, Sale, Worker,
                             Offer, BankData, Configuration)

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
admin.site.register(BankData)
admin.site.register(Configuration)
