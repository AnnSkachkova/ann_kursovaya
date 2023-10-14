from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from . import models


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