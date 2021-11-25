from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name= models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=150,unique=True)
    description=models.TextField(max_length=300,blank=True)
    images=models.ImageField(upload_to='photo/brand')
    stock=models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.brand_name 



