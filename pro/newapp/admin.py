from django.contrib import admin
from newapp.models import Catagory,Product

# Register your models here.

# class CatagoryAdmin(admin.ModelAdmin):
#     list_display=('name','image','description')
# admin.site.register(Catagory,CatagoryAdmin)


admin.site.register(Catagory)
admin.site.register(Product)