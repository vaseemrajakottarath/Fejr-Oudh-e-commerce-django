from django.shortcuts import render,redirect
from account.models import Account
from category.models import Category
from offer.form import CategoryOfferForm, ProductOfferForm
from store.models import Product
from store.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.contrib.auth.models import auth
from brand.models import Brand
from orders.models import OrderProduct,Ordern
from orders.forms import OrderProductForm
from django.utils import timezone
import datetime
from django.db.models import Sum
from offer.models import ProductOffer,CategoryOffer
from datetime import date ,timedelta
# Create your views here.

@login_required
def admindash(request):
    if request.user.is_authenticated:
        
        #sales or orders
        products=Product.objects.all().count()
        categories = Category.objects.all().count()
        users = Account.objects.all().count()

        total_orders = Ordern.objects.filter(is_ordered=True).count()
        total_revenue = Ordern.objects.aggregate(Sum('order_total'))
        total_sales_amount = float(total_revenue['order_total__sum'])
        current_year= timezone.now().year
        current_month = timezone.now().month
        order_detail = OrderProduct.objects.filter(created_at__month=current_month, status = 4)

         #daily bookings
        today = date.today()
        today_1 = today - timedelta(days=1)
        today_2 = today - timedelta(days=2)
        today_3 = today - timedelta(days=3)
        today_4 = today - timedelta(days=4)
        today_5 = today - timedelta(days=5)
        today_6 = today - timedelta(days=6)
        today_7 = today - timedelta(days=7)
        tomorrow = today + timedelta(days=1)

        last_week_days=[
            today_6.strftime("%a %m/%d/%Y"),
            today_5.strftime("%a %m/%d/%Y"),
            today_4.strftime("%a %m/%d/%Y"),
            today_3.strftime("%a %m/%d/%Y"),
            today_2.strftime("%a %m/%d/%Y"),
            today_1.strftime("%a %m/%d/%Y"),
            today.strftime("%a %m/%d/%Y"),]

        print(last_week_days)        
        today_order      =   OrderProduct.objects.filter(created_at__range=[today,tomorrow]).count()
        today_1_order    =   OrderProduct.objects.filter(created_at__range=[today_1,today]).count()
        today_2_order    =   OrderProduct.objects.filter(created_at__range=[today_2,today_1]).count()
        today_3_order    =   OrderProduct.objects.filter(created_at__range=[today_3,today_2]).count()
        today_4_order    =   OrderProduct.objects.filter(created_at__range=[today_4,today_3]).count()
        today_5_order    =   OrderProduct.objects.filter(created_at__range=[today_5,today_4]).count()
        today_6_order    =   OrderProduct.objects.filter(created_at__range=[today_6,today_5]).count()
         

        lastweek_orders=[today_6_order,today_5_order,today_4_order,today_3_order,today_2_order,today_1_order,today_order]
        print(lastweek_orders)
        #status
        order_accepted = OrderProduct.objects.filter(status=1).count()
        shipped = OrderProduct.objects.filter(status=2).count()
        out_for_delivery = OrderProduct.objects.filter(status=3).count()
        delivered = OrderProduct.objects.filter(status=4).count()
        cancelled_count = OrderProduct.objects.filter(status=0).count()
        #most moving product
        # most_moving_product_count = list()
        # most_moving_product = list()
        # for i in products:
        #     most_moving_product.append(i)
        #     most_moving_product_count.append(OrderProduct.objects.filter(product=i, status=4).count())
        context = {
            'order_detail':order_detail,
            'status_counter':[order_accepted,shipped,out_for_delivery,delivered,cancelled_count],
            # 'most_moving_product_count':most_moving_product_count,
            # 'most_moving_product':most_moving_product,
            'last_week_days':last_week_days,
            'lastweek_orders':lastweek_orders,
            'total_orders':total_orders,
            'products':products,
            'categories':categories,
            'users':users,
            'total_sales_amount':round(total_sales_amount),
            'order_detail':order_detail,
        }
        return render(request,'adminpanel/index.html',context)
    
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
        # product_image2=request.POST and request.FILES['image2']
        # product_image3=request.POST and request.FILES['image3']
        product_stock=request.POST['stock']
        product_category=request.POST.get('category')
        if Product.objects.filter(product_name=product_name).exists():
            print("Existing product")
            
            return redirect('addproduct')
        else:
            category = Category.objects.get(pk=product_category)
            add_product=Product.objects.create(product_name=product_name,slug=product_slug,description=product_description,images=product_image,
            # image2=product_image2,image3=product_image3,
            price=product_price,stock=product_stock,category=category)
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
        # brand_stock         = request.POST['brand_stock']
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
        # brand_stock        = request.POST['brand_stock']
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

def order_list(request):
    order_list=OrderProduct.objects.all()
    context={
        'order_list':order_list
    }
    return render(request,'adminpanel/order_list.html',context)

def order_history(request):
    order_history = OrderProduct.objects.all()
    context = {
        'order_history':order_history,
    }
    return render(request,'adminpanel/order_history.html',context)

def editorder(request,product_id):
    order_list=OrderProduct.objects.get(id=product_id)
    form=OrderProductForm(instance=order_list)
    if request.method=='POST':
        form=OrderProductForm(request.POST,instance=order_list)
        if form.is_valid():
            try:
                form.save()
            except:
                context={'form':form}
                return render(request,'adminpanel/order_edit.html',context)
            return redirect('order_list')
    context={'form':form}
    return render(request,'adminpanel/order_edit.html',context)

def cancelorder(request,order_product_id):
    order=OrderProduct.objects.get(id=order_product_id)
    order.delete()

    return redirect('order_list')

def product_offer(request):
    productoffer=ProductOffer.objects.all()
    context={
        'productoffer':productoffer,
    }
    return render(request,'adminpanel/product_offer.html',context)

def editproductoffer(request,offer_id):
    list_order_product=ProductOffer.objects.get(id=offer_id)
    form = ProductOfferForm(instance=list_order_product)
    if request.method == 'POST':
        form = ProductOfferForm(request.POST,request.FILES,instance=list_order_product)
        print(form)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form':form}
                return render(request,'adminpanel/editoffer.html',context)
            return redirect('product_offer')
    context = {'form':form}     
    return render(request,'adminpanel/editoffer.html',context)

def deleteproductoffer(request,offer_id):
    product_offer=ProductOffer.objects.get(id=offer_id)
    product_offer.delete()
    return redirect('product_offer')

def add_productoffer(request):
    form = ProductOfferForm()
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_offer')
    context = {
            'form':form,
    }
    return render(request,'adminpanel/add_productoffer.html',context)

def category_offer(request):
    category_offer = CategoryOffer.objects.all()
    context ={
        'category_offer':category_offer,
    }
    return render(request,'adminpanel/category_offer.html',context)

def deletecategoryoffer(request,offer_id):
    category_list=CategoryOffer.objects.get(id=offer_id)
    category_list.delete()
    return redirect('category_offer')


def editcategoryoffer(request,offer_id):
    category = CategoryOffer.objects.get(id=offer_id)
    form = CategoryOfferForm(instance=category)
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form':form}
                return render(request,'adminpanel/editcategoryoffer.html',context)
            return redirect('category_offer')
    context = {'form':form}
    return render(request,'adminpanel/editcategoryoffer.html',context)

def add_categoryoffer(request):
    form = CategoryOfferForm()
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_offer')
    context = {
            'form':form,
    }
    return render(request,'adminpanel/add_categoryoffer.html',context)
