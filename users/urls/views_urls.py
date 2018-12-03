from __future__ import absolute_import
from django.urls import path
from .. import views
from django.conf.urls import url


app_name = 'users'

urlpatterns = [
    # Login view

    # User view
    path('user/', views.UserListView.as_view(), name='user-list'),
    url(r'^register/', views.register, name='register'),

]