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


from TPVpnapp.models import Client, Product, Sale, Worker

from rest_framework import serializers

'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('url','username','email')


class FullDirectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = FullDirection
    fields = (
      'location', 'province', 'postalCode', 'direction',
      'numDir', 'stairs', 'numFlat', 'door'
    )

'''


class WorkerSerializer(serializers.ModelSerializer):
    # vdirection = FullDirectionSerializer(read_only=True)
    class Meta:
        model = Worker
        fields = ('dni', 'market')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'provider', 'category', 'subcategory',
                  'sellPrice', 'amount', 'iva', 'market', 'barCode', 'image')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'image', 'dni', 'wallet')


class SaleSerializer(serializers.ModelSerializer):
    # buyer = ClientSerializer(read_only=True)
    seller = WorkerSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'totAmount', 'date', 'benefice', 'seller')
