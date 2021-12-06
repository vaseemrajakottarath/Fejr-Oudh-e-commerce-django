from django.contrib import admin
from django.db import models
from .models import Banner, Product,Variation,ReviewRating
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
admin.site.register(Product,ProductAdmin)

class  VariationAdmin(admin.ModelAdmin):
     list_display = ('product','variation_category','variation_value','is_active')
     list_editable=('is_active',)
     list_filter= ('product','variation_category','variation_value')

admin.site.register(Variation,VariationAdmin)

admin.site.register(ReviewRating)
admin.site.register(Banner)