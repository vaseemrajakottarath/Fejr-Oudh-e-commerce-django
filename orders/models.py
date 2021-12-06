from django.db import models
from account.models import Account
from store.models import Product,Variation

# Create your models here.
STATUS=(
    (1,'Order Confirmed'),
    (2,'Shipped'),
    (3,'Out for delivery'),
    (4,'order delivered'),
    (0,'cancelled'),
)

class Payment(models.Model):
    user= models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid= models.CharField(max_length=100)   
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.payment_id

# class  Order(models.Model):

#     STATUS = (
#         ('New', 'New'),
#         ('Accepted', 'Accepted'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     )

#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
#     order_number = models.CharField(max_length=20)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField(max_length=50)
#     address_line_1 = models.CharField(max_length=50)
#     address_line_2 = models.CharField(max_length=50, blank=True)
#     country = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     order_note = models.CharField(max_length=100, blank=True)
#     order_total = models.FloatField()
#     tax = models.FloatField()
#     status = models.CharField(max_length=10, choices=STATUS, default='New')
#     ip = models.CharField(blank=True, max_length=20)
#     is_ordered = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
    
#     def full_address(self):
#         return f'{self.address_line_1} {self.address_line_2}'


#     def __str__(self):
#         return self.first_name

class Ordern(models.Model):

    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=20)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=200)
    alternate_phone = models.CharField(max_length=200)
    order_number = models.CharField(max_length=200)
    order_total = models.FloatField()
    tax = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Ordern, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations =models.ManyToManyField(Variation,blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    status=models.IntegerField(choices=STATUS,default=1)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

class Address(models.Model):
    TYPE=(
        ('home','home'),
        ('work','work'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=20)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=200)
    alternate_phone = models.CharField(max_length=200)
    type = models.CharField(max_length=200,choices=TYPE)
    

