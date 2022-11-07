from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter
from . import views
from pprint import pprint

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
pprint(router.urls)


# first way :
urlpatterns = router.urls

# if you want to have some other paths

# urlpatterns = [
#     path('', include(router.urls)),
#     # path()....
# ]

  