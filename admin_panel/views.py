from django.shortcuts import render,redirect
from account.models import Account
from category.models import Category
from store.models import Product
from store.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.contrib.auth.models import auth
from brand.models import Brand
# Create your views here.

@login_required
def admindash(request):
    return render(request,'adminpanel/index.html')




def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(password=password, email=email, is_superadmin=True)       
        print(user,email,password)
        if user is not None:
            if user.is_superadmin:
                auth.login(request, user)
                return redirect('admindash')
            else:
                return redirect('adminlogin')  
        else:
            return redirect('adminlogin')
    return render(request,'adminpanel/login.html')


def category(request):
    category=Category.objects.all()
    context={
        'category':category
    }



    return render(request,'category.html',context)
def product(request):
    product=Product.objects.all()
    context={
        'product':product
    }
    return render(request,'adminpanel/product.html',context)

def deletecategory(request,cat_id):

    categories = Category.objects.get(id=cat_id)
    print(categories)
    categories.delete()
    return redirect('category')

def deleteproduct(request,cat_id):
 
    product = Product.objects.get(id=cat_id)
  
    product.delete()
    return redirect('product')

def editcat(request,cat_id):
    list_cats = Category.objects.get(id=cat_id)
    print(list_cats)
    context = { 'list_cats' : list_cats }
    if request.method == 'POST':
        category_Name         = request.POST['category_Name']
        category_slug         = request.POST['category_slug']
        category_Description  = request.POST['category_Description']
        
        list_cats.category_name  = category_Name
        list_cats.slug           = category_slug
        list_cats.description    = category_Description
        list_cats.save()
        
        return redirect('category')
    return render(request,'editcat.html',context)

def addcat(request):
    if request.method=='POST':
        category_Name = request.POST['category_Name']
        category_slug         = request.POST['category_slug']
        category_Description  = request.POST['category_Description']
        if Category.objects.filter(category_name=category_Name).exists():
            # messages.info(request,'Category name taken')
            return redirect('addcat')
        else:
            add_cat = Category.objects.create(category_name=category_Name,slug=category_slug,description=category_Description)
            add_cat.save()
            return redirect('category')
        
    return render(request,'addcat.html')

def editproduct(request,cat_id):
    list_prod=Product.objects.get(id=cat_id)
    form=ProductForm(instance=list_prod)
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=list_prod)
        if form.is_valid():
            try:
                form.save()
            except:
                context= {'form':form}
                return render(request,'adminpanel/editproduct.html')


def editproduct(request,cat_id):
        list_prod = Product.objects.get(id=cat_id)
        form = ProductForm(instance=list_prod)
        if request.method=='POST':
            form=ProductForm(request.POST,request.FILES,instance=list_prod)
            if form.is_valid():
                try:
                    form.save()                
                except:
                    context = {'form':form}
                    return render(request,'adminpanel/editproduct.html',context)
                return redirect('product')

        context = {'form':form}  
        return render(request,'adminpanel/editproduct.html',context)

def addproduct(request):
    categories=Category.objects.all()
    if request.method=='POST':
        product_name = request.POST['product_name']
        product_slug =request.POST['product_slug']
        product_description=request.POST['product_description']
        product_price=request.POST['price']
        product_image=request.POST and request.FILES['images']
        product_stock=request.POST['stock']
        product_category=request.POST.get('category')
        if Product.objects.filter(product_name=product_name).exists():
            print("Existing product")
            
            return redirect('addproduct')
        else:
            category = Category.objects.get(pk=product_category)
            add_product=Product.objects.create(product_name=product_name,slug=product_slug,description=product_description,
            price=product_price,images=product_image,stock=product_stock,category=category)
            add_product.save()
            return redirect('product')
    print(categories)
    context={'categories':categories}

    return render(request,'adminpanel/addproduct.html',context)

def brand(request):
    brand=Brand.objects.all()
    context={'brand':brand}
    return render(request,'adminpanel/brand.html',context)

def deletebrand(request,cat_id):
    brand=Brand.objects.get(id=cat_id)
    brand.delete()
    return redirect('brand')


def editbrand(request,cat_id):
    list_brands = Brand.objects.get(id=cat_id)
    print(list_brands)
    context = { 'list_brands' : list_brands}
    if request.method == 'POST':
        brand_name         = request.POST['brand_name']
        brand_slug         = request.POST['brand_slug']
        brand_stock         = request.POST['brand_stock']
        brand_Description  = request.POST['brand_description']
        
        list_brands.brand_name  = brand_name
        list_brands.slug           = brand_slug
        list_brands.stock=brand_stock
        list_brands.description    = brand_Description
        list_brands.save()
        
        return redirect('brand')
    return render(request,'editbrand.html',context)   

def addbrand(request):
    if request.method=='POST':
        brand_name = request.POST['brand_name']
        brand_slug         = request.POST['brand_slug']
        brand_stock        = request.POST['brand_stock']
        brand_description  = request.POST['brand_description']
        if Brand.objects.filter(brand_name=brand_name).exists():
            # messages.info(request,'Category name taken')
            return redirect('addbrand')
        else:
            add_brand = Brand.objects.create(brand_name=brand_name,slug=brand_slug,stock=brand_stock,description=brand_description)
            add_brand.save()
            return redirect('brand')
        
    return render(request,'adminpanel/addbrand.html')

def usermanage(request):
    account=Account.objects.all()
    context={'account':account}
    return render(request,'adminpanel/usermanage.html',context)

def deleteuser(request,user_id):
    user=Account.objects.get(id=user_id)
    user.delete()
    return redirect('usermanage')

def blockuser(request,user_id):
    userdata=Account.objects.get(id=user_id)
    if userdata.is_active:
        userdata.is_active=0
        userdata.save()
    return redirect('usermanage')

def unblockuser(request,user_id):
    userdata=Account.objects.get(id=user_id)
    if  not userdata.is_active:
        userdata.is_active=1
        userdata.save()
    return redirect('usermanage')