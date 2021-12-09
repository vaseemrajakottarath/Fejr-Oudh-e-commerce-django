from django.contrib import admin
from .models import BrandOffer, Coupon, ProductOffer,CategoryOffer, RedeemedCoupon

# Register your models here.
class ProductOfferAdmin(admin.ModelAdmin):
    list_display=('product','discount_offer','is_active')
class CategoryOfferAdmin(admin.ModelAdmin):
    list_display=('category','discount_offer','is_active')

class CouponAdmin(admin.ModelAdmin):
    list_display=('coupon_code','discount','is_active')

class RedeemedCouponAdmin(admin.ModelAdmin):
    list_display=('user','coupon')

admin.site.register(ProductOffer,ProductOfferAdmin)
admin.site.register(CategoryOffer,CategoryOfferAdmin)
admin.site.register(BrandOffer)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(RedeemedCoupon,RedeemedCouponAdmin)