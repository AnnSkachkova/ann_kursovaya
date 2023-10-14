from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from . import models
from django.http.response import FileResponse
from utils import model_to_xls


class Login(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self) -> str:
        user = self.request.user
        token = self.request.POST['user_token']
        models.Token.objects.update_or_create(user=user, defaults={'token': token})
        return super(Login, self).get_success_url()


class Logout(LogoutView):
    next_page = reverse_lazy('login')


class HomePage(TemplateView):
    template_name = 'index.html'
    

class ProductPage(TemplateView):
    template_name = 'products.html'
    

class ContractorPage(TemplateView):
    template_name = 'contractors.html'
    

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