from django.urls import path
from rest_framework import routers
from . import views


app_name = 'api'


urlpatterns = [
    
]


routers = routers.SimpleRouter()
routers.register('products', views.ProductViewSet, basename='products')
