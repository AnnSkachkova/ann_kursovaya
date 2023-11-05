from typing import Any
from django.contrib.auth.views import LoginView, LogoutView
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, View, UpdateView, ListView
from django.urls import reverse_lazy, reverse
from . import models
from django.http.response import FileResponse
from utils import model_to_xls
from django.db.models import Sum, F, Q
from .forms import ContractorForm


class Login(LoginView):
    template_name = 'falcon/login.html'
    
    def get_success_url(self) -> str:
        user = self.request.user
        token = self.request.POST['user_token']
        models.Token.objects.update_or_create(user=user, defaults={'token': token})
        return reverse('main:index')
    
    

class Logout(LogoutView):
    next_page = reverse_lazy('login')


class HomePage(TemplateView):
    template_name = 'falcon/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context["product_count"] = models.Product.objects.count()
        context['contractor_count'] = models.Contractor.objects.count()
        product_count_field = F('count')
        product_price_field = F('product__price')
        context["total_cost"] = models.StorageItem.objects.aggregate(tc=Sum(product_count_field * product_price_field))['tc']
        context["contractors"] = models.Contractor.objects.all()
        return context
    

class ProductList(ListView):
    template_name = 'falcon/products.html'
    model = models.Product
    paginate_by = 10
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["products"] = models.Product.objects.all()
    #     return context
    
   

class ContractorPage(TemplateView):
    template_name = 'contractors.html'
    

class ContractorUpdate(UpdateView):
    form_class = ContractorForm
    model = models.Contractor
    template_name = ''
    
    def post(self, request, *args,**kwargs):
        if self.request.POST:
            formset = ContractorForm(self.request.POST)
            
            if formset.is_valid():
                formset.save()
                
        return super().post(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user
        
    def get_success_url(self) -> str:
        return reverse()
    
    def form_valid(self, form):
        form.save()
        return super(ContractorUpdate, self).form_valid(form)
    
    
    

class DocumentPage(TemplateView):
    template_name = 'documents.html'
    

class OperationPage(TemplateView):
    template_name = 'operations.html'
    

class StorageItemPage(TemplateView):
    template_name = 'storage_items.html'


class RemoveMarkedObjects(TemplateView):
    template_name = 'remove_marked_objects.html'


class ImportProduct(TemplateView):
    template_name = 'import_products.html'
    

class ConsolidatedReport(TemplateView):
    template_name = 'consolidated_report.html'
    
    
    
    
    
class MotionReport(TemplateView):
    template_name = 'motion_report.html'
    
    def get_context_data(self, **kwargs):
        context = super(MotionReport, self).get_context_data(**kwargs)
        context["report_type"] = self.request.GET['report_type']
        return context


def products_to_xls(request):
    column_descriptions = [
        {'machine_name': 'id', 'display_name': 'Номер'},
        {'machine_name': 'title', 'display_name': 'Наименование', 'width': 80},
        {'machine_name': 'description', 'display_name': 'Описание', 'width': 30},
        {'machine_name': 'price', 'display_name': 'Цена'},
        {'machine_name': 'dt_created', 'display_name': 'Дата создания', 'width': 30},
        {'machine_name': 'dt_updated', 'display_name': 'Дата изменения', 'width': 30},
    ]
    xls_data = model_to_xls(models.Product, column_descriptions)

    return FileResponse(
        xls_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename='product.xlsx'
    )


def contractors_to_xls(request):
    column_descriptions = [
        {'machine_name': 'id', 'display_name': 'Номер'},
        {'machine_name': 'title', 'display_name': 'Наименование', 'width': 80},
        {'machine_name': 'category', 'display_name': 'Категория', 'width': 30,
         'subs': dict(models.Contractor.CONTRACTOR_CATEGORY)},
        {'machine_name': 'dt_created', 'display_name': 'Дата создания', 'width': 30},
        {'machine_name': 'dt_updated', 'display_name': 'Дата изменения', 'width': 30},
    ]
    xls_data = model_to_xls(models.Contractor, column_descriptions)

    return FileResponse(
        xls_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename='products.xlsx'
    )