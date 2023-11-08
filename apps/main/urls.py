from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    path('', login_required(views.HomePage.as_view()), name='index'),
    path('products/', login_required(views.ProductList.as_view()), name='products'),
    path('contractors/', login_required(views.ContractorList.as_view()), name='contractors'),
    path('documents/', login_required(views.DocumentList.as_view()), name='documents'),
    path('operations/', login_required(views.OperationList.as_view()), name='operations'),
    path('storage_items/', login_required(views.StorageItemList.as_view()), name='storage_items'),
    path('remove_marked_objects/', login_required(views.RemoveMarkedObjects.as_view()), name='remove_marked_objects'),
    path('import_products/', login_required(views.ImportProduct.as_view()), name='import_products'),
    path('consolidated_report/', login_required(views.ConsolidatedReport.as_view()), name='consolidated_report'),
    path('motion_report/', login_required(views.MotionReport.as_view()), name='motion_report'),
    path('products_to_xls/', login_required(views.products_to_xls), name='products_to_xls'),
    path('contractors_to_xls/', login_required(views.contractors_to_xls), name='contractors_to_xls'),
]