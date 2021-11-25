from django.db.models import fields
from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','slug','price','images','description','stock','is_available','category']