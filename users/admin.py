from django.contrib import admin
from .models import MyUser
# Register your models here.
#  自定义admin
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'source', 'last_login', 'date_joined']

admin.site.register(MyUser, MyUserAdmin)


