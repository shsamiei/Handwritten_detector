from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import Class_based_views


# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),

    

]
 