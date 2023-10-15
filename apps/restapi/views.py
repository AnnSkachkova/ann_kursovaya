import utils
from django.shortcuts import render
from rest_framework import viewsets
from django.db.models.query_utils import DeferredAttribute
from apps.main import models
from apps.restapi import serializers
from .pagination import CustomPagination
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


class RegisteredViewSet(viewsets.ModelViewSet):
    ...
    def _get_model_field_values(self, element):
        result = []
        for key in sorted(self.model.__dict__.keys()):
            value = self.model__dict__[key]
            if key != 'id' and isinstance(value, DeferredAttribute):
                result.append(getattr(element, key))
            return result
        
    def get_queryset(self):
        queryset = self.model.objects.all()
        order = self.request.query_params.get('order')
        if order:
            queryset = queryset.order_by(order)
        return queryset
    
    def create(self, request, *args, **kwargs):
        result = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        pk = result.data['id']
        created_element = self.model.objects.filter(pk=pk).first()
        if created_element:
            username = utils.get_username_for_operation(request.user)
            operation = f'Создан {self.model_verbose_name}: {created_element}'
            models.Operation.objects.create(username=username, operation=operation)
        return result

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        updated_element = self.model.objects.filter(pk=pk).first()
        result = viewsets.ModelViewSet.update(self, request, *args, **kwargs)
        if updated_element:
            to_remove_before = updated_element.to_remove
            main_fields_before = self._get_model_field_values(updated_element)
            updated_element.refresh_from_db()
            to_remove_after = updated_element.to_remove
            main_fields_after = self._get_model_field_values(updated_element)

            username = utils.get_username_for_operation(request.user)
            if main_fields_before != main_fields_after:
                print(main_fields_before)
                print(main_fields_after)

                operation = f'Изменен {self.model_verbose_name}: {updated_element}'
                models.Operation.objects.create(username=username, operation=operation)
            if not to_remove_before and to_remove_after:
                operation = f'{self.model_verbose_name} помечен на удаление: {updated_element}'
                models.Operation.objects.create(username=username, operation=operation)
            if to_remove_before and not to_remove_after:
                operation = f'Снята пометка на уделение с {self.model_verbose_name}: {updated_element}'
                models.Operation.objects.create(username=username, operation=operation)

        return result
    

class ProductViewSet(RegisteredViewSet):
    serializer_class = serializers.ProductSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title', 'description']

    model = models.Product
    model_verbose_name = 'Товар'