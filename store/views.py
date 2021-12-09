from django.shortcuts import render,get_object_or_404,redirect
from category.models import Category
from  store. models import Product,ReviewRating
from cart.models import CartItem
from orders.models import OrderProduct
from cart.views import _cart_id
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request,category_slug=None):
    Categories= None
    products=None
    if category_slug != None:
        Categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=Categories,is_available=True)
        paginator =Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator =Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count =products.count()

    context = {
        'products':paged_products,
        'product_count':product_count,
        }
    return render(request,'store/store.html',context)
        
def product_detail(request,category_slug,product_slug):
    try:
        single_product =Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
     
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None

    #Get the reviews
    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)

    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
    }

    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in  request.GET:
        keyword= request.GET['keyword']
        if keyword:
            products= Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword)|Q(product_name__icontains=keyword))
            product_count =products.count()
    context={
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)

def submit_review(request,product_id):
     url = request.META.get('HTTP_REFERER')
     if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def buy_now(request,product_id):
    if request.user.is_authenticated:
        product=Product.objects.get(id=product_id)
        request.session['direct_buy']=product.id
        return redirect('checkout')
    else:
        messages.error(request,'Please login')
        return redirect('store')