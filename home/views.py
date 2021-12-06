from django.shortcuts import render
from store.models import Banner, Product

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
