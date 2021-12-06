from django.db import models
from brand.models import Brand
from category.models import Category
from store.models import Product
from django.contrib.auth import get_user_model

# Create your models here.
class BrandOffer(models.Model):
    brand_name=models.OneToOneField(Brand,on_delete=models.CASCADE)
    discount_offer=models.PositiveIntegerField(help_text='Offer in percentage')
    is_active=models.BooleanField(default=True)

    def __init__(self):
        return self.brand_name
        
class ProductOffer(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    discount_offer=models.PositiveIntegerField(help_text='Offer in percentage')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)

class CategoryOffer(models.Model):
    category=models.OneToOneField(Category,on_delete=models.CASCADE)
    discount_offer=models.PositiveIntegerField(help_text='Offer in percentage')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)
class Coupon(models.Model):
    coupon_code= models.CharField(max_length=40,unique=True)
    discount = models.PositiveIntegerField(help_text="Offer in percentage", null=True)
    is_active = models.BooleanField(default=False)

class RedeemedCoupon(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    
    


        