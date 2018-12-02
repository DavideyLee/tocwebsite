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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),    # 设置超级管理员的路由
    url(r'^users/', include('django.contrib.auth.urls')),  # 设置内置的URL路由
    path('users/', include('users.urls.views_urls', namespace='users')),  # 设置自定义users的路由
    path('orgs/', include('orgs.urls.views_urls', namespace='orgs')),  # 设置自定义orgs的路由
    url(r'^$', views.index, name='index'),  # 设置自定义首页index页面URL的路由
]

#  静态资源（css、js）加载URL设置、头像URL加载设置
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
            + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)