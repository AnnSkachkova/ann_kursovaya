from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from . import models


class Login(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self) -> str:
        user = self.request.user
        token = self.request.POST['user_token']
        models.Token.objects.update_or_create(user=user, defaults={'token': token})
        return super(Login, self).get_success_url()


class HomePage(TemplateView):
    template_name = 'index.html'
    
