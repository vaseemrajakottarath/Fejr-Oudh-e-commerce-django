from django.contrib import admin
from . models import Brand

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand_name',)}
    list_display=('brand_name','slug','description','stock','is_available','modified_date')
admin.site.register(Brand,BrandAdmin)