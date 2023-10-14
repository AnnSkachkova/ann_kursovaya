from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    path('', login_required(views.HomePage.as_view()), name='index'),
    path('products/', login_required(views.ProductPage.as_view()), name='products'),
    path('contractors/', login_required(views.ContractorPage.as_view()), name='contractors')
]