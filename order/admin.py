from django.contrib import admin
from .models import *
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model=OrderProduct

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderProductInline]


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)