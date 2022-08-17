
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.cartview, name='cartview'),  
    path('add_cart/<int:product_id>/',views.add_cart, name='add_cart'),
    path('add_cartplus/<int:product_id>/',views.add_cartplus, name='add_cartplus'),

    
    path('buy_now/<int:product_id>/',views.buy_now, name='buy_now'), 

    path('add_cartsimple/<int:product_id>/',views.add_cartsimple, name='add_cartsimple'), 
    path('remove_cartminus/<int:product_id>/',views.remove_cartminus,name ='remove_cartminus' ),

    path('remove_cart/<int:product_id>/',views.remove_cart,name ='remove_cart' ),
    path('delete/<int:product_id>/',views.delete_carts,name ='delete_cart' ),
    path('delete_cartshome/<int:product_id>/',views.delete_cartshome,name ='delete_cartshome' ),

    path('deleteloggedin/<int:product_id>/',views.delete_cart_loggedin,name ='deleteloggedin' ),
    path('checkout',views.checkout,name='checkout'), 
    path('addaddress',views.addaddress,name='addaddress') , 
    path('addaddress1',views.addaddress1,name='addaddress1') , 
    path('confirmpayment',views.confirmpayment,name='confirmpayment') , 
    path('placecod',views.placecod,name='placecod') , 
    path('placecodBuynow',views.placecodBuynow,name='placecodBuynow') , 

    
    path('paypal',views.paypal,name='paypal'), 
    path('payments',views.payments,name='payments'),
    path('order_complete',views.order_complete,name='order_complete'),
    path('razorpayhome',views.razorpayhome,name='razorpayhome'),
    path('razorpaysuccess/',views.razorpaysuccess,name='razorpaysuccess'),
    path('couponapply',views.couponapply,name='couponapply'), 
    
 
     


    # path('success', views.paypal_success, name="success"),  
 

]
