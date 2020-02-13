"""rest_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

import xadmin

urlpatterns = [
    # post 登录JWT，获取token的url
    path('api-token-auth/',obtain_jwt_token),
    # post 刷新JWT的token 的url
    path('api-token-refresh/',refresh_jwt_token),
    # 认证token
    path('api-token-verify/',verify_jwt_token),

    # 给可浏览的API添加登录功能
    path('api-auth/',include("rest_framework.urls")),

    path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),

    path('rest/',include("rest_app.urls")),
    path('1.0/rest/',include("rest_app.urls"),namespace='1.0'),
    path('2.0/rest/',include("rest_app.urls"),namespace='2.0')
]
