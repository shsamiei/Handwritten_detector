from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views
from pprint import pprint


# it is nested router way : 

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + products_router.urls


  