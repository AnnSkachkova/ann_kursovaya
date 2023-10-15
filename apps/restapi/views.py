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
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response


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
    

class ContractorViewSet(RegisteredViewSet):
    serializer_class = serializers.ContractorSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title']

    model = models.Contractor
    model_verbose_name = 'Контрагент'
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contractor_categories(request):
    return Response(dict(models.Contractor.CONTRACTOR_CATEGORY))


class OperationViesSet(viewsets.ModelViewSet):
    serializer_class = serializers.OperationSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'operation']
    queryset = models.Operation.objects.all()
    

class StorageItemViewSet(RegisteredViewSet):
    serializer_class = serializers.StorageItemSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['product__id', 'product__title']

    model = models.StorageItem
    model_verbose_name = 'Товар на складе'

    def get_queryset(self):
        queryset = models.StorageItem.objects.all()
        order = self.request.query_params.get('order')
        if order:
            if order.endswith('product_title'):
                prefix = '-' if order.startswith('-') else ''
                queryset = queryset.order_by(f'{prefix}product__title')
            else:
                queryset = queryset.order_by(order)
        return queryset
    

class DocumentViewSet(RegisteredViewSet):
    serializer_class = serializers.DocumentSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    model = models.Document
    model_verbose_name = 'Документ'

    def get_queryset(self):
        queryset = models.Document.objects.all()

        # Обрабатываем параметры сортировки
        order = self.request.query_params.get('order')
        if order:
            if order.endswith('contractor_title'):
                prefix = '-' if order.startswith('-') else ''
                queryset = queryset.order_by(f'{prefix}contractor__title')
            else:
                queryset = queryset.order_by(order)

        # Обрабатываем параметры поиска
        number = self.request.query_params.get('number')
        if number:
            queryset = queryset.filter(pk=number)
        dt_start = self.request.query_params.get('dt_start')
        if dt_start:
            queryset = queryset.filter(dt_created__gte=dt_start)
        dt_end = self.request.query_params.get('dt_end')
        if dt_end:
            dt_end += " 23:59:59"
            queryset = queryset.filter(dt_created__lte=dt_end)
        contractor = self.request.query_params.get('contractor')
        if contractor:
            queryset = queryset.filter(contractor=contractor)
        destination_type = self.request.query_params.get('destination_type')
        if destination_type:
            queryset = queryset.filter(destination_type=destination_type)
        apply_flag = self.request.query_params.get('apply_flag')
        if apply_flag:
            apply_flag = apply_flag.lower()
            apply_flag = {'true': True, 'false': False}[apply_flag]
            queryset = queryset.filter(apply_flag=apply_flag)

        return queryset