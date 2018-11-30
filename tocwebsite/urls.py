"""tocwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from users import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),    # 设置超级管理员的路由
    url(r'^users/', include('users.urls')),  # 设置自定义users的路由
    url(r'^users/', include('django.contrib.auth.urls')), # 设置内置的URL路由
    url(r'^$', views.index, name='index'), # 设置自定义首页index页面URL的路由
]
