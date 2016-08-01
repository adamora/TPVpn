from django.contrib.auth.models import *
from TPVpnapp.models import *
from rest_framework import serializers

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

class WorkerSerializer(serializers.ModelSerializer):
  #direction = FullDirectionSerializer(read_only=True)
  class Meta:
    model = Worker
    fields = ('url','dni','market')

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = (
      'id','name','provider','category','subcategory',
      'sellPrice','amount','iva','market','barCode','image'
    )

class ClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = ('name','image','dni','wallet')

class SaleSerializer(serializers.ModelSerializer):
  #buyer = ClientSerializer(read_only=True)
  seller = WorkerSerializer(read_only=True)
  class Meta:
    model = Sale
    fields = ('id','totAmount','date','benefice','seller')
