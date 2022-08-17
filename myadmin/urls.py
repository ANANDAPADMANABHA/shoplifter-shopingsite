from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminLogin),
    path('adminhome',views.admin_home,name='adminhome'),
    path('admintable',views.admin_table,name='admintable'),
    path('productlist/',views.productList, name='productlist'),
    path('category',views.categoryList,name='category'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('delete/<int:id>/',views.deleteproduct,name='delete'),
    path('addproduct',views.addproduct,name='addproduct'), 
    path('signout',views.adminLogout,name='signout'),  
    path('addcategory',views.addcategory) ,
    path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),
    path('blockuser/<int:id>/',views.blockuser,name='blockuser'),
    path('orderdisplay',views.orderdisplay,name='orderdisplay') , 
    path('orderstatus/<int:id>/',views.orderstatus,name='orderstatus')  ,
    path('offerstatus/<int:id>/',views.offerstatus,name='offerstatus')  ,
    path('offerstatusedit/<int:id>/',views.offerstatusedit,name='offerstatusedit')  ,
    
    path('searchprod',views.searchprod,name='searchprod')  , 
    path('orderdetailsadmin/<int:id>/',views.orderdetailsadmin,name='orderdetailsadmin') ,
    path('couponlist',views.couponlist,name='couponlist') , 
    path('disableorenablecoupon/<int:id>/',views.disableorenablecoupon,name='disableorenablecoupon') ,
    path('couponadd',views.couponadd,name='couponadd') ,
    path('salesreport',views.salesreport,name='salesreport') ,
    path('date_range',views.date_range,name='date_range') ,

    
    path('monthly_report/<int:date>/',views.monthly_report,name='monthly_report'),
    path('yearly_report/<int:date>/',views.yearly_report,name='yearly_report') ,
    
    path('product-chart/', views.product_chart, name='product-chart'),
    path('payment-chart/', views.payment_chart, name='payment-chart'),
    path('adminbanner', views.adminbanner, name='adminbanner'),
    path('addbanner', views.addbanner, name='addbanner'),
    path('deletebanner/<int:id>/', views.deletebanner, name='deletebanner'),
    path('selectbanner/<int:id>/', views.selectbanner, name='selectbanner'),
    path('offermanage', views.offermanage, name='offermanage'),
    path('productoffermanage', views.productoffermanage, name='productoffermanage'),
    path('categoryoffermanage', views.categoryoffermanage, name='categoryoffermanage'),

    path('disablecatoffer/<int:id>/', views.disablecatoffer, name='disablecatoffer'),
    path('offerstatuseditproduct/<int:id>/', views.offerstatuseditproduct, name='offerstatuseditproduct'),
    path('disableprodoffer/<int:id>/', views.disableprodoffer, name='disableprodoffer'),

    

    
    
    


] 
