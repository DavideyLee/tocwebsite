from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    # url(r'^user/add/$', 'user_add', name='user_add'),
    # url(r'^user/del/$', 'user_del', name='user_del'),
    url(r'^user/list/$', views.user_list, name='user_list'),
    # url(r'^user/edit/$', 'user_edit', name='user_edit'),
    # url(r'^user/detail/$', 'user_detail', name='user_detail'),
    # url(r'^user/profile/$', 'profile', name='user_profile'),
    # url(r'^user/update/$', 'change_info', name='user_update'),
]