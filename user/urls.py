from django.urls import path
from . import views

urlpatterns = [
    path('',views.home ,name='userhome' ),
    path('signinuser',views.signin,name='signinuser'),
    path('usersignup',views.userSignup,name='usersignup'), 
    path('usersignin',views.userSignin ,name='usersignin'),
    path('otp',views.otplogin ,name='otp'),
    path('otpenter<int:Phone_num>',views.otpenter, name='otpenter'),
    path('phone_number_verification<str:username>',views.phone_number_verification, name='phone_number_verification'),
    path('otpentersignup<int:Phone_num>',views.otpentersignup, name='otpentersignup'),
    path('singnupuser',views.userSignup),
    path('userlogout',views.userlogout,name='userlogout'),
    path('productdisplay<int:id>',views.productDisplay,name='productdisplay') ,
    path('userprofile',views.userprofile,name='userprofile'), 
    path('myorders',views.myorders,name='myorders'), 
    path('ordercancel/<int:id>/',views.ordercancel,name='ordercancel') ,
    path('changepassword',views.changepassword,name='changepassword'),  
    path('search',views.search,name='search'),  
    path('homecart',views.homecart,name='homecart'),  
    path('shoplaptop',views.shoplaptop,name='shoplaptop'),  
    path('shopphone',views.shopphone,name='shopphone'), 
    path('shopheadphone',views.shopheadphone,name='shopheadphone'), 
    path('shoptab',views.shoptab,name='shoptab'), 
    path('limiteddeal',views.limiteddeal,name='limiteddeal'),  
    path('demand',views.demand,name='demand'),  
    
    
    path('addressdelete/<int:id>/',views.addressdelete,name='addressdelete') ,
    path('editaddress/<int:id>/',views.editaddress,name='editaddress') ,



    
    path('orderdetails/<int:id>/',views.orderdetails,name='orderdetails'),
    path('orderreturn/<int:id>/',views.orderreturn,name='orderreturn')  
 

 




    
    




]