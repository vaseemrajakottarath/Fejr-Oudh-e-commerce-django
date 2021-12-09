from django.shortcuts import render,redirect
from store.models import Banner, Product
from django.contrib import messages

# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True)
    banner=Banner.objects.all()
    print(banner)
    context ={
        'products':products,
        'banner':banner,
    }
    return render(request,'home.html',context)
# def signin(request):
#     return render(request,'signin.html')
# def register(request):
#     return render(request,'register.html')
def buy_now(request,product_id):
    if request.user.is_authenticated:
        product=Product.objects.get(id=product_id)
        request.session['direct_buy']=product.id
        return redirect('checkout')
    else:
        messages.error(request,'Please login')
        return redirect('store')
