from django.db.models import fields
from django.forms import ModelForm
from .models import Banner, Product, ReviewRating
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','slug','price','images','description','stock','is_available','category']

class ReviewForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject','review','rating']

class BannerForm(forms.ModelForm):
    class Meta:
        model=Banner
        fields=['image','product','is_active','alternate_text']
    