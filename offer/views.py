from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from offer.models import Coupon, RedeemedCoupon
from django.contrib import messages

def coupon(request):
    user=request.user
    if request.method=='POST':
        coupon_code = request.POST['coupon_code']
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code,is_active=True)
        except:
            messages.error(request,'Invalid Coupon')
            return redirect('checkout')

        try:
            redeemed_coupon = RedeemedCoupon.objects.get(user=user, coupon=coupon)
        except:
            redeemed_coupon=None

        if redeemed_coupon is None:
            discount = coupon.discount
            request.session['coupon_id']= str(coupon.id)
            request.session['coupon_discount']=discount
            messages.success(request, 'Coupon Applied')
            return redirect('checkout')
        else:
            messages.error(request,'Already redeemed this coupon')
            return redirect('checkout')
    else:
        return redirect('checkout')