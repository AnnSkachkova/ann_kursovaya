from django.shortcuts import render, HttpResponse
from django.contrib.auth.views import LoginView


class Login(LoginView):
    template_name = 'login.html'


def index(request):
    return HttpResponse("ghbsdfsdfsdf")