"""trigger_alert_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from links_app import urls
from links_app.views import UserRegistrationView
from links_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('admin/', admin.site.urls),
    path('links/', include(urls)),

    path('api-auth/', include('rest_framework.urls')),
    url('signup/', UserRegistrationView.as_view()),
    path('api/token/',  obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('validate_username/',views.validateUsername)
]
