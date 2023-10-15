from django.urls import path
from rest_framework import routers
from . import views


app_name = 'api'


urlpatterns = [
    path('contractor_categories/', views.contractor_categories, name='contractor_categories'),
]


router = routers.SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('contractors', views.ContractorViewSet, basename='contractors')
