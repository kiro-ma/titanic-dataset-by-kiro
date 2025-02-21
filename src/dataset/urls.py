from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = []

router = DefaultRouter()
router.register(r'dataset', DatasetViewSet)

urlpatterns = urlpatterns + router.urls
