from django.contrib import admin
from .models import Event
# Register your models here.
#  自定义admin
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'even_state' ,'even_level', 'even_ops', 'even_dev',  'created_time', 'modified_time' ]

admin.site.register(Event, EventAdmin)
