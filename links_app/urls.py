from django.urls import path, include
from rest_framework import routers
from links_app import views

router = routers.DefaultRouter()
router.register('user', views.LinkViewSet, basename='user')
router.register('all', views.LinkProcessorViewSet, basename='all')

urlpatterns = [
    path('', include(router.urls)),
]