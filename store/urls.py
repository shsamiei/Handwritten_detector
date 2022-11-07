from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views


# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>', views.product_detail),
    path('collections/<int:pk>', views.collection_detail, name='collection-detail'),
    

]
