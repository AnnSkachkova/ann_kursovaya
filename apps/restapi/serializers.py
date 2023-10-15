from rest_framework import serializers
from apps.main import models


class ProductSerializer(serializers.ModelSerializer):
    ...
    class Meta:
        model = models.Product
        fields = '__all__'
        

class ContractorSerializer(serializers.ModelSerializer):
    ...
    class Meta:
        model = models.Contractor
        fields = '__all__'
        

class OperationSerializer(serializers.ModelSerializer):
    ...
    class Meta:
        model = models.Operation
        fields = ['username', 'operation', 'dt_created']
        

class StorageItemSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        result['product_title'] = instance.product.title
        result['product_price'] = instance.product.price
        return result

    class Meta:
        model = models.StorageItem
        fields = '__all__'
        

class DocumentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        result['contractor_title'] = instance.contractor.title
        return result

    class Meta:
        model = models.Document
        fields = '__all__'