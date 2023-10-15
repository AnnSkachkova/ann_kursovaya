from rest_framework import serializers
from apps.main import models


class ProductSerializer(serializers.ModelSerializer):
    ...
    class Meta:
        model = models.Product
        fields = '__all__'
        