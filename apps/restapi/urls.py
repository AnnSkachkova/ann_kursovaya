from django.urls import path
from rest_framework import routers
from . import views


app_name = 'api'


urlpatterns = [
    path('contractor_categories/', views.contractor_categories, name='contractor_categories'),
    path('apply_document/<int:document_id>/', views.apply_document, name='apply_document'),
    path('unapply_document/<int:document_id>/', views.unapply_document, name='unapply_document'),
    path('remove_marked_objects/', views.remove_marked_objects, name='remove_marked_objects'),
    path('import_products/', views.import_products, name='import_products'),
    path('consolidated_report/', views.consolidated_report, name='consolidated_report'),
    path('motion_report/', views.motion_report, name='motion_report'),
]


router = routers.SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('contractors', views.ContractorViewSet, basename='contractors')
router.register('operations', views.OperationViesSet, basename='operations')
router.register('documents', views.DocumentViewSet, basename='documents')
router.register('document_items', views.DocumentItemViewSet, basename='document_items')
router.register('storage_items', views.StorageItemViewSet, basename='storage_items')
urlpatterns.extend(router.urls)