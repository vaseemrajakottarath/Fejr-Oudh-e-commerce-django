from django.contrib import admin
from .models import BrandOffer, Coupon, ProductOffer,CategoryOffer, RedeemedCoupon

# Register your models here.

admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(BrandOffer)
admin.site.register(Coupon)
admin.site.register(RedeemedCoupon)