


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.conf import settings
import json
from django.contrib import messages
import datetime
from django.shortcuts import redirect, render
from theproducts.models import Product
from accounts.models import Account , Address
from cartapp.models import Cart, CartItem
from orders.models import OrderProduct, Orders, Payment
from datetime import date 
from user.views import *
# from user.views import home


from django.views.decorators.cache import cache_control
# from user.views import 
from django.template.loader import render_to_string
# from weasyprint import HTML

import tempfile
 



def _cart_id(request):
    session_id = request.session.session_key
    if not session_id:
        session_id    =   request.session.create()
    return session_id

def add_cart(request , product_id):
    
    product = Product.objects.get(id=product_id) #get the product
    

    if request.user.is_authenticated:
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user,cartprice=product.offer_price() )
            cart_item.save()
    else:
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart,cartprice=product.offer_price())
            cart_item.save()

    

    return redirect (cartview)

def buy_now(request,product_id):
    if request.user.is_authenticated:
        cartclear = CartItem.objects.filter(buy_now = True , user = request.user)
        cartclear.delete()
        product = Product.objects.get(id = product_id)
        cart = CartItem(product = product,quantity=1,user = request.user,cartprice=product.offer_price(),buy_now = True)
        cart.save()
        return redirect(checkout)
    else :
        return redirect(signin)

def add_cartplus(request , product_id):
    total = 0
    quantity = 0
    
    product = Product.objects.get(id=product_id) #get the product
    

    if request.user.is_authenticated:
        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user,cartprice=product.offer_price() )
            cart_item.save()

        try:
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")
            
            for cart_item in cart_items:
            
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax -reduction
                  
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'tax':round(tax,2),
        'cart_items':cart_items,
        'quantity':quantity,
        'grand_total':grand_total
        }
    else:
        
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart,cartprice=product.offer_price())
            cart_item.save()

        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True).order_by("-id")
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax 
            
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'tax':round(tax,2),
        'cart_items':cart_items,
        'quantity':quantity,
        'grand_total':grand_total
        
        }

    return render (request,'htmx_cart.html',context)

#to add times to the cart without entering the cart from the index page
def add_cartsimple(request , product_id):
    
    product = Product.objects.get(id=product_id) #get the product
    

    if request.user.is_authenticated:
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user,cartprice=product.offer_price())
            cart_item.save()
    else:
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart,cartprice=product.offer_price())
            cart_item.save()
    return redirect ("userhome")

def couponapply(request):
    print('+++++++++++++++++++++++++++++++++')
    if request.method == 'POST':
        print('===================================')
        coupon_code = request.POST.get('coupon_code')
        try:
            if Coupon.objects.get(coupon_code=coupon_code):
                coupon_exist =Coupon.objects.get(coupon_code=coupon_code)
                try:
                    
                    if UsedCoupon.objects.get(user=request.user,coupon = coupon_exist):
                        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                        messages.error(request,"coupon already used")
                        return redirect(cartview)
                    
                        
                except:
                    request.session['coupon_code']=coupon_code
        except:
            pass
    return redirect(cartview)




def cartview(request,total = 0, quantity = 0, cart_items =None,tax = 0,grand_total =0):

    cartclear = CartItem.objects.filter(buy_now = True , user = request.user)
    cartclear.delete()
    
    if request.user.is_authenticated:

        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0

        
        try:
            
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True,buy_now = False).order_by("-id")
            
            
            
            for cart_item in cart_items:
            
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax -reduction
            if grand_total <0:
                grand_total = tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True).order_by("-id")
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':round(tax,2),
        'grand_total':grand_total,
        }
    
    
    return render (request,'cart.html' ,context)

def remove_cartminus(request, product_id):

    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    if request.user.is_authenticated:
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(user =request.user, product= product)

        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.cartprice -= cart_items.product.offer_price() 
            cart_items.save()

        else:
            cart_items.delete() 
        
    else:

        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(product= product, cart = cart)

        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.cartprice -= cart_items.product.offer_price() 
            cart_items.save()

        else:
            cart_items.delete()

    if request.user.is_authenticated:

        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0

        
        try:
            
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")
            
            for cart_item in cart_items:
            
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax -reduction
            if grand_total <0:
                grand_total = tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':round(tax,2),
        'grand_total':grand_total,
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True).order_by("-id")
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':round(tax,2),
        'grand_total':grand_total,
        }

    return render (request,'htmx_cart.html',context)
    
    

def remove_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(user =request.user, product= product)

        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.cartprice -= cart_items.product.offer_price() 
            cart_items.save()

        else:
            cart_items.delete() 
        return redirect('cartview')
    else:

        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(product= product, cart = cart)

        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.cartprice -= cart_items.product.offer_price() 
            cart_items.save()

        else:
            cart_items.delete()
        return redirect('cartview')

def delete_cartshome(request, product_id):
    total = 0
    quantity = 0
    cart_items = CartItem.objects.get(id =product_id )
    cart_items.delete()
    if request.user.is_authenticated:
        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0

        try:    
            try:
                counts = CartItem.objects.filter(user = request.user, is_active = True).count()
            except:
                counts = 0
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")[0:2]
            
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax -reduction
            if grand_total <0:
                grand_total = tax
        except ObjectDoesNotExist:
            pass #just ignore
    
    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            try:
                counts  = CartItem.objects.filter(cart = cart, is_active = True).count()
            except:
                counts = 0

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            counts = 0
            pass #just ignore

    context = {
        
        'quantity':quantity,
        'cart_items':cart_items,
        'x':counts,
        'grand_total':grand_total,
        }
    return render (request, "htmx_deletehome.html",context)


def delete_carts(request, product_id):
    total = 0
    quantity = 0
    
    
    cart_items = CartItem.objects.get(id =product_id )
    cart_items.delete()

    if request.user.is_authenticated:
        try:
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")
            
            for cart_item in cart_items:
            
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
                  
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'cart_items':cart_items,
        'quantity':quantity,
        'tax':tax,
        
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
            
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
       'tax':tax,
        'cart_items':cart_items,
        'quantity':quantity,
        
        }
    return render (request,'htmx_cart.html',context)

def delete_cart(request, product_id):
    # if request.method == "POST":


        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(product= product, cart = cart)

    
        cart_items.delete()
        


        return redirect('cartview')

def delete_cart_loggedin(request, product_id):
    # if request.method == "POST":
        print("##################################################")
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(user = request.user,product= product)
        cart_items.delete()
        try:
             CartItem.objects.get(user = request.user)
        except:
        
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
                
            

        return redirect('cartview')

def checkout(request):
    
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    
    if request.user.is_authenticated:
        cart_itemscount  = CartItem.objects.filter(user = request.user, is_active = True).count()
        if cart_itemscount >  0:


            if 'coupon_code' in request.session:
                print('couponnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
                coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
                reduction = coupon.discount 

            else :
                reduction = 0


            try:
                details = Address.objects.filter(user = request.user )
                cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
                if CartItem.objects.filter(user = request.user,buy_now = True) :
                    cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)
                for cart_item in cart_items:
                    total += (cart_item.product.offer_price() * cart_item.quantity)
                    quantity += cart_item.quantity
                tax = (2*total)/100
                grand_total = total + tax-reduction
                if grand_total <0:
                    grand_total = tax
            except ObjectDoesNotExist:
                pass #just ignore
        else:
            return redirect('userhome')

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':round(tax,2),
        'grand_total':round(grand_total,2),
        'details':details,
        }

    else:
        
        return redirect("signinuser")
    return render(request,'checkout.html',context)


def addaddress(request):
    if request.method == "POST":
        firstname    = request.POST.get('firstname')
        lastname    = request.POST.get('lastname')
        housename    = request.POST.get('housename')
        locality    = request.POST.get('locality')
        city    = request.POST.get('city')
        state    = request.POST.get('state')
        pincode    = request.POST.get('pincode')
        phonenumber    = request.POST.get('phonenumber')
        pincode    = request.POST.get('pincode')

        address = Address(firstname=firstname,lastname=lastname,housename=housename,locality=locality,city=city,state=state,pincode=pincode,phonenumber=phonenumber,user = request.user)
        
        address.save()

        return redirect(checkout)
    return render(request,'addaddress1.html')
def addaddress1(request):
    if request.method == "POST":
        firstname    = request.POST.get('firstname')
        lastname    = request.POST.get('lastname')
        housename    = request.POST.get('housename')
        locality    = request.POST.get('locality')
        city    = request.POST.get('city')
        state    = request.POST.get('state')
        pincode    = request.POST.get('pincode')
        phonenumber    = request.POST.get('phonenumber')
        pincode    = request.POST.get('pincode')

        address = Address(firstname=firstname,lastname=lastname,housename=housename,locality=locality,city=city,state=state,pincode=pincode,phonenumber=phonenumber,user = request.user)
        
        address.save()

        return redirect ("userprofile")
    return render(request,'addaddress1.html')



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def confirmpayment(request):
    if request.method == "POST":
        global theaddress
        theaddress = request.POST.get('address') #address object in the address as we passed address in it
   
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    
    if request.user.is_authenticated:

        if 'coupon_code' in request.session:
            print('couponnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0


        try:
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            if CartItem.objects.filter(user = request.user,buy_now = True) :
                    cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)
                    Buynow = True
            else:
                Buynow = False
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax-reduction
            if grand_total <0:
                grand_total = tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'details':details,
        'Buynow':Buynow
        
        }
        

    else:
        return redirect(cartview)
    return render(request,'confirmorderinvoice.html',context)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def placecodBuynow(request):

    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    if request.user.is_authenticated:

        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0
        try:

            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            
            user =  request.user
            
            if CartItem.objects.filter(user = request.user,buy_now = True) :
                cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)
            
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                tax = (2*total)/100
            grand_total = total + tax-reduction
            if grand_total <0:
                grand_total = tax
                

            dates =date.today()   
            paymethod = 'COD'
            pay = Payment(user=request.user,payment_method =paymethod,amount_paid=grand_total ,status='Pending',created_at=dates)
            pay.save()

            oder = Orders(user=user,address=details ,ordertotal = total,orderid =order_id_generated,date=dates,payment =pay)
            oder.save()

            
            
            
            for x in cart_items:
                order = Orders.objects.get(orderid = order_id_generated)
                Orderproduct = OrderProduct(order=order)
                product = Product.objects.get(id = x.product.id)
                Orderproduct.product = x.product
                Orderproduct.quantity = x.quantity
                Orderproduct.price = x.cartprice
                product.stock -=  x.quantity
                product.save()
                Orderproduct.save()
                

            for x in cart_items:
                x.delete()
            
        except :

            redirect("userhome")

        
    else:
        return redirect(cartview)
    try:    
        order = Orders.objects.get(orderid = order_id_generated)
        order.is_ordered = True
        order.save()
        Orderproduct = OrderProduct.objects.filter(order=order)

        if 'coupon_code' in request.session:
            coupons = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            x = UsedCoupon(user = request.user , coupon =coupons )
            x.save()
            del request.session['coupon_code']
            
    except:
        return redirect("userhome")
    context = {
    'total':total,
    'quantity':quantity,
    'Orderproduct':Orderproduct,
    'tax':tax,
    'grand_total':pay.amount_paid,
    'details':details,
        }

    return render(request,'bill.html',context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def placecod(request):

    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    if request.user.is_authenticated:

        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0
        try:

            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            
            user =  request.user
            
           
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            cart_itemcount = cart_items.count()
            if cart_itemcount <= 0 :
                return redirect('userhome')
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                tax = (2*total)/100
            grand_total = total + tax-reduction
            if grand_total <0:
                grand_total = tax
                

            dates =date.today()   
            paymethod = 'COD'
            pay = Payment(user=request.user,payment_method =paymethod,amount_paid=grand_total ,status='Pending',created_at=dates)
            pay.save()

            oder = Orders(user=user,address=details ,ordertotal = total,orderid =order_id_generated,date=dates,payment =pay)
            oder.save()

            
            
            for x in cart_items:
                order = Orders.objects.get(orderid = order_id_generated)
                Orderproduct = OrderProduct(order=order)
                product = Product.objects.get(id = x.product.id)
                Orderproduct.product = x.product
                Orderproduct.quantity = x.quantity
                Orderproduct.price = x.cartprice
                product.stock -=  x.quantity
                product.save()
                Orderproduct.save()
                

            for x in cart_items:
                x.delete()
            
        except ObjectDoesNotExist:
            pass #just ignore

        
    else:
        return redirect(cartview)
        
    order = Orders.objects.get(orderid = order_id_generated)
    order.is_ordered = True
    order.save()
    Orderproduct = OrderProduct.objects.filter(order=order)

    if 'coupon_code' in request.session:
        coupons = Coupon.objects.get(coupon_code =request.session['coupon_code'])
        x = UsedCoupon(user = request.user , coupon =coupons )
        x.save()
        del request.session['coupon_code']
            
    context = {
    'total':total,
    'quantity':quantity,
    'Orderproduct':Orderproduct,
    'tax':tax,
    'grand_total':pay.amount_paid,
    'details':details,
        }

    return render(request,'bill.html',context)


# -------------------------------------------------------------------------------------------------------------
def paypal(request):
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    if request.user.is_authenticated:
        try:

            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            user =  request.user
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            if CartItem.objects.filter(user = request.user,buy_now = True) :
                    cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)
            cart_itemcount = cart_items.count()
            if cart_itemcount <= 0 :
                return redirect('userhome')
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
            tax = (2*total)/100
            grand_total = total + tax
                
            oder = Orders(user=user,address=details ,ordertotal = grand_total,orderid =order_id_generated)
            oder.save()

            
            
            order = Orders.objects.get(orderid = order_id_generated)
            Orderproduct = OrderProduct.objects.filter(order=order)
            context = {
                    'cart_items':cart_items,
                    'order' :order,
                    "order_id_generated" :order_id_generated,
                    'total':total,
                    'quantity':quantity,
                    'Orderproduct':Orderproduct,
                    'tax':tax,
                    'grand_total':grand_total,
                    'details':details,
        
                        }
            return render(request, 'paypal.html',context)

            
            

        except ObjectDoesNotExist:
            pass #just ignore

        
        

    else:
        return redirect(cartview)
        
    

def payments(request):
    body = json.loads(request.body)
    order = Orders.objects.get(orderid = body['orderID'] )
    payment = Payment(

        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.ordertotal,
        status = body['status'],
    )
    payment.save()
    print(body)
    order.payment = payment
    order.is_ordered =True
    order.save()
    #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
    cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
    if CartItem.objects.filter(user = request.user,buy_now = True) :
        cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)
    for x in cart_items:
                
        Orderproduct = OrderProduct(order=order)
        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.price = x.product.price
        Orderproduct.save()
    #REDUCE THE QUANTITY OF STOCK

        product = Product.objects.get(id = x.product.id)
        product.stock -= x.quantity
        product.save()
    #CLEAR CART
    
    cart_items.delete()
    #SEND ORDER RECIEVED EMAIL TO CUSTOMER

    #SEND ORDER NUMBER AND TRANSACTION ID BACK TO SEND DATA METHOD VIA JASON RESPONDS
    data = {
        "orderID":order.orderid,
        "transID":payment.payment_id,
    }


    return JsonResponse(data)


def order_complete(request):
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    order_number    = request.GET.get("orderID")
    transID         = request.GET.get("transID")
    print(order_number)

    try:
        dates =date.today()   
        details = Address.objects.get(id = theaddress )
        order = Orders.objects.get(orderid = order_number)
        order.is_ordered = True
        order.save()
        ordered_products = OrderProduct.objects.filter(order = order)
        Orderproduct = OrderProduct.objects.filter(order=order)
        for cart_item in Orderproduct:
            total += (cart_item.product.offer_price() * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

        context = {
            "order":order,
            "ordered_products":ordered_products,
            "orderID":order.orderid,
            "details":details,
            "transID":transID,
            "dates":dates,
            "grand_total":grand_total,
            "tax":tax,
            "total":total
        }
        return render(request,"order_complete.html",context)

    except (Payment.DoesNotExist,Orders.DoesNotExist):
        return redirect("userhome")
# -------------------------------------------------------------------------------------------------------
def razorpayhome(request):
    total = 0
    cart_items  = CartItem.objects.filter(user = request.user, is_active = True) 
    if CartItem.objects.filter(user = request.user,buy_now = True) :
        cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)

    for cart_item in cart_items:
        total += (cart_item.product.offer_price() * cart_item.quantity)

    # if request.method == "POST":
        
        
        client = razorpay.Client(auth=(settings.KEY , settings.SECRET ))

        payment = client.order.create({ 
                "amount": total*100,
                "currency": "INR",  
                "payment_capture": 1,
                # "receipt": "receipt#1",  
                # "account_id": "acc_Ef7ArAsdU5t0XL" 
                })
        
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(payment)
        context = {
            'cart': cart_items, 
            'payment' : payment
                }
    return render(request,'razorpayhome.html',context)

            
def razorpaysuccess(request):
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0

    pay_id = request.GET.get('razorpay_payment_id')
    try:
        if 'coupon_code' in request.session:
            print('couponnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0
        #place payment
        cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
        if CartItem.objects.filter(user = request.user,buy_now = True) :
                cart_items  =   CartItem.objects.filter(user = request.user,buy_now = True)
        cart_itemcount = cart_items.count()
        if cart_itemcount <= 0 :
            return redirect('userhome')
        for cart_item in cart_items:
            total += (cart_item.product.offer_price() * cart_item.quantity)
        tax = (2*total)/100
        grand_total = total + tax-reduction
        if grand_total <0:
                grand_total = tax
        dates =date.today()
        
        pay = Payment(user = request.user,payment_id =pay_id,payment_method= 'Razorpay',amount_paid=grand_total,status='COMPLETED',created_at=dates)
        pay.save()


        #place order
        details = Address.objects.get(id = theaddress )
        order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        order = Orders(user = request.user,address = details,ordertotal =total,orderid=order_id_generated,date=dates ,payment=pay,status='Confirmed',is_ordered = True)
        order.save() 

        #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
        
        for x in cart_items:
            Orderproduct = OrderProduct(order=order)
            Orderproduct.product = x.product
            Orderproduct.quantity = x.quantity
            Orderproduct.price = x.product.offer_price()
            Orderproduct.save()

        #REDUCE THE QUANTITY OF STOCK

            product = Product.objects.get(id = x.product.id)
            product.stock -= x.quantity
            product.save()
            
        
        cart_items.delete()
        
        #for context
        
        Orderproduct = OrderProduct.objects.filter(order=order)
        if 'coupon_code' in request.session:
            coupons = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            x = UsedCoupon(user = request.user , coupon =coupons )
            x.save()
            del request.session['coupon_code']
        
        context = {
            "order":order,
            "ordered_products":Orderproduct,
            "orderID":order.orderid,
            "details":details,
            "pay_id":pay_id,
            "dates":dates,
            "grand_total":pay.amount_paid,
            "tax":tax,
            "total":total
        }
        
        return render(request,'razorpaysuccess.html',context)

    except (Payment.DoesNotExist,Orders.DoesNotExist):
        return redirect("userhome")

    
    
