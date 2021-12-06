from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from cart.models import CartItem
from orders.models import  OrderProduct, Payment,Ordern
from . forms import OrderForm,AddressForm
import datetime,json
import razorpay
from django.conf import settings
from store.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import EmailMessage
from offer.models import Coupon,RedeemedCoupon
from django.template.loader import render_to_string
from django.http import JsonResponse
razorpay_client=razorpay.Client(
    auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))


# Create your views here.
def orders(request,total=0,quantity=0):
    current_user= request.user

    # if cart count is less than  or equal to zero
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if request.session.has_key('couponid'):
        print("inside fir")
        couponid=request.session['couponid']
        coupon=Coupon.objects.get(id=couponid)
        if coupon.is_active==True:
            coupon_redeem=RedeemedCoupon()
            coupon_redeem.user=current_user
            coupon_redeem.coupon=coupon
            coupon_redeem.save()
    if cart_count <= 0:
        return redirect('store')

    grand_total =0
    tax=0
    total_savings=0
    offer_savings=0
    item=None
    for cart_item in cart_items:
        total += (cart_item.product.get_price() * cart_item.quantity)
        offer_savings=total-(cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax

    if request.session.has_key('couponid'):
        print('inside Coupen')
        # couponid=request.session['coupon_id']
        # request.session['couponid']=couponid
        # del request.session['coupon_id']
        coupen_discount= request.session['coupon_discount']
        coupen_discount_price = total*(coupen_discount)/100
        grand_total=grand_total-coupen_discount_price
        total_savings=grand_total-(coupen_discount_price-offer_savings)
        print(grand_total)
    else:
        coupen_discount_price=0

    total_savings= grand_total-(coupen_discount_price-offer_savings)
    if request.method =='POST':
        print("inside if")
        form =OrderForm(request.POST)
        if form.is_valid():

            #store all billing information inside order table
            data = Ordern()
            data.user = current_user
            data.name = form.cleaned_data['name']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.locality = form.cleaned_data['locality']
            data.landmark = form.cleaned_data['landmark']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.pincode = form.cleaned_data['pincode']
            data.alternate_phone = form.cleaned_data['alternate_phone']
            data.order_total = grand_total
            data.tax = tax
            data.save()
            #Generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number= current_date + str(data.id)
            data.order_number = order_number
            data.save()
            request.session['order_number']=order_number
            request.session['grand_total']=grand_total
            order_amount = int(grand_total*100)
            print(order_amount)
            order_currency = 'INR'
            razorpay_order = razorpay_client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture='0'))
            payment_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'

            order= Ordern.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'payment_order_id': payment_order_id,
                'razorpay_amount':order_amount,
                'currency':order_currency,
                'callback_url' : callback_url,
                'total_savings':total_savings,
                'coupen_discount_price':coupen_discount_price,
            }
            return render(request,'store/payments.html',context)
    
    else:
        return redirect('checkout')
    return HttpResponse("some")

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()




            
def payments(request):
    body = json.loads(request.body)
    print(body)
    order = Ordern.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    #store transaction details inside Payment method
    payment =Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment =payment
    order.is_ordered=True
    order.save()

    #Move cart items to Order Product table
    cart_items=CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id =order.id
        orderproduct.payment =payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered =True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        #Reduce the quantity of the sold products

        product=Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear cart
    CartItem.objects.filter(user=request.user).delete()

    # send order recieved email to  customer
    mail_subject = 'Thank you for your order'
    message = render_to_string('order_recieved_mail.html', {
                'user': request.user,
                'order':order,
                
            })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def order_complete(request):
   order_number = request.session['order_number']
   del request.session['order_number']
   transID = request.GET.get('payment_id')

   try:
        order = Ordern.objects.get(order_number=order_number, is_ordered=False)
        ordered_products = OrderProduct.objects.get(order_id=order.id)
        order.is_ordered=True
        order.save()
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'order_complete.html', context)
   except Exception as e:
               print(e)
               try:
                    order = Ordern.objects.get(order_number=order_number, is_ordered=True)
                    ordered_products = OrderProduct.objects.filter(order_id=order.id)

                    subtotal = 0
                    for i in ordered_products:
                        subtotal += i.product_price * i.quantity

                    payment = Payment.objects.get(payment_id=transID)

                    context = {
                        'order': order,
                        'ordered_products': ordered_products,
                        'order_number': order.order_number,
                        'transID': payment.payment_id,
                        'payment': payment,
                        'subtotal': subtotal,
                    }
                    return render(request, 'order_complete.html', context)
               except:
                    try:
                        order = Ordern.objects.get(order_number=order_number, is_ordered=True)
                        ordered_products = OrderProduct.objects.filter(order_id=order.id)

                        subtotal = 0
                        for i in ordered_products:
                            subtotal += i.product_price * i.quantity
                        razorpay_order_id=request.session['razorpay_order_id']
                        payment = Payment.objects.get(payment_id=razorpay_order_id)

                        context = {
                            'order': order,
                            'ordered_products': ordered_products,
                            'order_number': order.order_number,
                            'transID': payment.payment_id,
                            'payment': payment,
                            'subtotal': subtotal,
                        }
                        return render(request, 'order_complete.html', context)
                    except (Ordern.DoesNotExist):
                        return redirect('home')
                
       

def user_orders(request,total=0,quantity=0):
    # tax=0
    # grand_total=0
    orders=Ordern.objects.filter(user=request.user,is_ordered=True).order_by('created_at')
    orderproduct=OrderProduct.objects.filter(user=request.user)
    cart_items=CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:
        total += (cart_item.product.get_price() * cart_item.quantity)
        quantity += cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax
    
    context={
        'orders':orders,
        'orderproduct':orderproduct,
        'grand_total':grand_total,  
       
        }
    return render(request,'orders/my_orders.html',context)



def order_details(request,order_id):
    orderproduct=OrderProduct.objects.get(id=order_id)
    context={
        'orderproduct':orderproduct
    }
    return render(request,'orders/details.html',context)

def cancel_order(request,order_id):
    try:
        orders=Ordern.objects.get(id=order_id,user=request.user)
        orderproduct=OrderProduct.objects.get(user=request.user,order=orders)
        item_id=orderproduct.product.id
        product=Product.objects.get(id=item_id)
        product.stock += orderproduct.quantity
        orderproduct.status = 0
        orderproduct.save()
        product.save()
    except:
        print("out")

    return redirect('user_orders')

def razorpay(request):
    currency = 'INR'
    amount = 20000

        # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
    currency=currency,payment_capture='0'))


    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

def cash_on_delivery(request,total=0,quantity=0):
    # move cartitems to orderproduct table
    order_number=request.session['order_number']
    order= Ordern.objects.get(user=request.user,is_ordered=False,order_number=order_number)
    cart_items=CartItem.objects.filter(user=request.user)


    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()


        cart_item=CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        #reduce the quantity of the product 
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # order.is_ordered=True
    # order.save()

    #clear cart
    CartItem.objects.filter(user=request.user).delete()
    return redirect('order_complete')

def payment_failed(request):
    # return render(request,'payment_failed.html')
    return HttpResponse("failed")

def razorpay_payment_verification(request):
    order_number=request.session['order_number']
    order = Ordern.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {

            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        request.session['razorpay_order_id']=razorpay_order_id
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except:
            return JsonResponse({'messages': 'error'})
    # Store transaction details inside Payment model
        payment = Payment(
            user = request.user,
            payment_id = razorpay_order_id,
            payment_method = 'rezorpay',
            amount_paid = order.order_total,
            status ='Completed',
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


    #     # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # # Clear cart
    CartItem.objects.filter(user=request.user).delete()
    return JsonResponse({'message': 'success'})