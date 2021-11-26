from django.contrib import messages,auth
from django.shortcuts import redirect, render,get_object_or_404

from cart.models import Cart, CartItem
from .verifyf import verify, verify2
from account.forms import RegistrationForms,UserProfileForm,UserForm
from account.models import Account,UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from cart.views import _cart_id
import requests
from orders.models import Order, OrderProduct

# Create your views here.
@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user= auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting product variation by cart id
                    product_variation =[]
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from user  to access his product variation

                    cart_item = CartItem.objects.filter(user=user)


                    ex_var_list =[]
                    id = []
                    for item in cart_item:

                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                    
                    #product_variation =[1,2,3,4]
                    #ex_var_list = [4,3,5,6]
                    for pro in product_variation:
                        if pro in ex_var_list:
                            index = ex_var_list.index(pro)
                            item_id =id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()


                    
            except:
                pass    
            auth.login(request,user)
            url=request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('signin')
    
    
    return render(request,'signin.html')
@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        if form.is_valid():
            first_name= form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number= form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username =email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()

            #  create user profile 
            profile=UserProfile()
            profile.user_id =user.id
            profile.save()

            messages.success(request,'Registration Successful.')
            return redirect('signin')
    else:

        form=RegistrationForms
    context ={
        'form':form
    }
    return render(request,'register.html',context)

@login_required(login_url =' signin')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('signin')

@never_cache
def numberotp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        mob=request.POST['phone']
        if Account.objects.filter(phone_number=mob).exists():
            verify(mob)
            request.session['checknumber']=mob
            return redirect('otp')
        else:
            messages.info(request,"phone number not registered")
            return redirect('numberotp')
    return render(request,'otpregister.html')

@never_cache
def otp(request):
    if request.method=='POST':
        otp=request.POST['otpnumber']
        mobile=request.session['checknumber']
        if verify2(mobile,otp):
            print("OTP verified")
            return redirect('signin')
        else:
            print("OTP not matching")
        
        
    return render(request,'otplogin.html')

def forgetpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)


            current_site = get_current_site(request)
            mail_subject='Reset Your Password'
            message = render_to_string('resetpassword_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email =email
            send_email =EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('signin')
            
        else:
            messages.error(request, 'Account does not exist!')  
            print("Not a registered email address")   
    return render(request,'forget.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('signin')

def resetpassword(request):
     if request.method == 'POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password == confirm_password:
            uid=request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull')
            return redirect('signin')
        else:
            messages.error(request,'Password do not match!')
            return redirect('resetpassword')
     else:
        return render(request,'resetpassword.html')

def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    context={
        'orders_count':orders_count,
    }
    return render(request,'dashboard.html',context)

@login_required(login_url =' signin')
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,'my_orders.html',context)

@login_required(login_url ='signin')
def edit_profile(request):

    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request,'edit_profile.html',context)


@login_required(login_url ='signin')
def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user =Account.objects.get(username__exact=request.user.username)

        if new_password==confirm_password:
            sucess=user.check_password(current_password)
            if sucess:
                user.set_password(new_password)
                user.save()
                
                # auth.logout(request)

                messages.success(request,'Password Changed Successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('chane_password.html')

    else:
        messages.error(request,'Password does not match X')
    return render(request,'change_password.html')

@login_required(login_url ='signin')
def order_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    subtotal=0
    for x in order_detail:
        subtotal += x.product_price * x.quantity

    context={
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
    }
    return render(request,'order_detail.html',context)