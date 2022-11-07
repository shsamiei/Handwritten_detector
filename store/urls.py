from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views


# URLConf
urlpatterns = [
    path('product/', views.product_list)

]
