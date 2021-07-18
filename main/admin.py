from django.contrib import admin
from .models import ToDoList, Item, RainTable, RainDay
# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(RainTable)
admin.site.register(RainDay)