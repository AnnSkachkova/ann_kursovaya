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