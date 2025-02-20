from django.urls import path, include
from .views import Home, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', Home.as_view()),
    path('', include(router.urls))
]