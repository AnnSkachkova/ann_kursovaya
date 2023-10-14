from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    path('', login_required(views.HomePage.as_view()), name='index'),
    path('products/', login_required(views.ProductPage.as_view()), name='products'),
    path('contractors/', login_required(views.ContractorPage.as_view()), name='contractors'),
    path('operations/', login_required(views.OperationPage.as_view()), name='operations'),
    path('storage_items/', login_required(views.StorageItemPage.as_view()), name='storage_items'),
    path('products_to_xls/', login_required(views.products_to_xls), name='products_to_xls'),
    path('contractors_to_xls/', login_required(views.contractors_to_xls), name='contractors_to_xls'),
]