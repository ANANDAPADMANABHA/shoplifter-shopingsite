from .models import Cart, CartItem, Coupon
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def extras(request,total = 0, quantity = 0, cart_items =None,tax = 0,grand_total =0):

    if request.user.is_authenticated:
        if 'coupon_code' in request.session:
            
            coupon = Coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupon.discount 

        else :
            reduction = 0

        try:    
            try:
                counts = CartItem.objects.filter(user = request.user, is_active = True,buy_now = False).count()
            except:
                counts = 0
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True,buy_now = False).order_by("-id")[0:2]
            
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
                counts  = CartItem.objects.filter(cart = cart, is_active = True,buy_now = False).count()
            except:
                counts = 0

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True,buy_now = False)
            for cart_item in cart_items:
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            counts = 0
            pass #just ignore

    context = {
        
        'quantitycontext':quantity,
        'cart_itemscontext':cart_items,
        'x':counts,
        'grand_totalcontext':round(grand_total,2),
        }

    return dict(context)


