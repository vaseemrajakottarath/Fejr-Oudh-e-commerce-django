from django.db import models
from django.db.models.deletion import CASCADE
from account.models import Account
from category.models import Category
from django.urls import reverse
from django.db.models.aggregates import Sum
from django.db.models import Avg, Count
from django.utils import timezone
from django.apps import apps

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price =models.IntegerField(null=True)
    tax=models.IntegerField(null=True)
    images=models.ImageField(upload_to='photo/products',null=True)
    image2=models.ImageField(upload_to='photo/products',null=True)
    image3=models.ImageField(upload_to='photo/products',null=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
                        
    def get_price(self):

        try:
            if self.productoffer.is_active:
                offer_price=(self.price/100) * self.productoffer.discount_offer
                product_price=self.price-offer_price
                return product_price
            raise
        except:
            try:
                if self.product.category.categoryoffer.is_active:
                    offer_price = (self.price / 100) * self.product.category.categoryoffer.discount_offer
                    product_price = self.price - offer_price
                    return product_price
                raise
            except:
                pass
            return self.price


    def __str__(self):  
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
            return avg

    def countReview(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
            return count
    
    def get_revenue(self,month=timezone.now().month):
        
        orderproduct = apps.get_model('orders', 'OrderProduct')
        orders=orderproduct.objects.filter(product=self,created_at__month=month,status=4)
        return orders.values('product').annotate(revenue=Sum('product_price'))
    
    def get_profit(self,month=timezone.now().month):
        
        orderproduct = apps.get_model('orders', 'OrderProduct')
        orders=orderproduct.objects.filter(product=self,created_at__month=month,status=4)
        profit_calculted=orders.values('product').annotate(profit=Sum('product_price'))
        profit_calculated=profit_calculted[0]['profit']*0.23
        return profit_calculated

    def get_count(self,month=timezone.now().month):
        orderproduct = apps.get_model('orders', 'OrderProduct')
        orders=orderproduct.objects.filter(product=self,created_at__month=month,status=4)
        return orders.values('product').annotate(quantity=Sum('quantity'))

class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice=(
    ('size','size'),
)



class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category =models.CharField(max_length=100,choices=variation_category_choice)
    variation_value= models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date= models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=200,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Banner(models.Model):
    image=models.ImageField(upload_to='photos/banners',blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    alternate_text=models.CharField(max_length=100)
    
    def __str__(self):
        return self.alternate_text