from django import   forms
from django.forms import fields
from .models import Order,Address

class OrderForm(forms.ModelForm):
    class Meta  :
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','order_note']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields =['name','phone','address','pincode','locality','city','state','landmark','alternate_phone','type']
    
    def __init__(self, *args, **kwargs):
        super(AddressForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'