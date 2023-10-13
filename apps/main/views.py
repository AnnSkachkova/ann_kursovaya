from django.shortcuts import render, HttpResponse
from django.contrib.auth.views import LoginView
from . import models


class Login(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self) -> str:
        user = self.request.user
        token = self.request.POST['user_token']
        models.Token.objects.update_or_create(user=user, defaults={'token': token})
        return super(Login, self).get_success_url()


def index(request):
    return HttpResponse("ghbsdfsdfsdf")