from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('menu/', views.index, name='index')
]