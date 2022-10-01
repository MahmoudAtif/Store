from django.contrib import admin

from .models import *

# Register your models here.
class ProductImagesInline(admin.TabularInline):
    model=ProductImages

class VariantsInline(admin.TabularInline):
    model=Variant
    

class ProductAdmin(admin.ModelAdmin):
    # list_display=['name','price']
    # list_filter=['price']
    inlines=[ProductImagesInline,VariantsInline]



admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImages)
# admin.site.register(Brand)
admin.site.register(Setting)
admin.site.register(ContactMessage)
admin.site.register(Comment)
admin.site.register(ShopCart)
admin.site.register(Variant)
admin.site.register(Size)
admin.site.register(Color)

