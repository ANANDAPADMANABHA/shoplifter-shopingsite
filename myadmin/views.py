
from datetime import datetime
import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.models import Account
from cartapp.models import Coupon
from myadmin.models import Banner
from orders.models import OrderProduct, Orders, Payment
from theproducts.models import Product , Categoryies
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator 
from django.http import JsonResponse

# Create your views here.

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def adminLogin(request):
    if 'username' in request.session:
        return redirect(admin_home)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username,password=password)

        if user is not None:
            if user.is_superuser:
                request.session['username']=username
                login(request,user)
                global count
                count = 0
                return redirect(admin_home)
        else:
            messages.error(request,'invalid credentials')
            return redirect(adminLogin)

    return render (request,'login_admin.html')


def adminLogout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(adminLogin)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_home(request):
    if 'username' in request.session:
        orders = Payment.objects.all()
        order = Payment.objects.filter(payment_method = 'COD')
        codtotal = 0
        cod = 0
        for ord in order:
            codtotal = codtotal+float(ord.amount_paid)
            cod+= 1

        raz = 0
        order = Payment.objects.filter(payment_method = 'Razorpay')   
        raztotal = 0
        for ord in order:
            raztotal = raztotal+float(ord.amount_paid) 
            raz+= 1
            
        order = Payment.objects.filter(payment_method = 'Paypal')   
        paytotal = 0
        pay = 0
        for ord in order:
            paytotal = paytotal+float(ord.amount_paid) 
            pay+= 1

        total =  paytotal + raztotal +  codtotal
        #order derails
        Confirmed = OrderProduct.objects.filter(status = 'Confirmed').count()
        Shipped = OrderProduct.objects.filter(status = 'Shipped').count()
        Out_for_delivery = OrderProduct.objects.filter(status = 'Out_for_delivery').count()
        Delivered = OrderProduct.objects.filter(status = 'Delivered').count()
        Cancelled = OrderProduct.objects.filter(status = 'Cancelled').count()
        Returned = OrderProduct.objects.filter(status = 'Returned').count()
        


        context = {
            'orders':orders,
            'codtotal':int(codtotal),
            'paytotal':int(paytotal),
            'raztotal':int(raztotal),
            'total':int(total),
            'pay':pay,
            'raz':raz,
            'cod':cod,
            'Confirmed':Confirmed,
            'Shipped':Shipped,
            'Out_for_delivery':Out_for_delivery,
            'Delivered':Delivered,
            'Cancelled':Cancelled,
            'Returned':Returned,

        }
       

        return render(request,'index_admin.html',context)

    return redirect(adminLogin)

def product_chart(request):
    labels = []
    data = []
    queryset = Product.objects.filter().order_by('name')[:8]
    for product in queryset:
        labels.append(product.name)
        data.append(product.price)
    print(data,labels)

    return JsonResponse(data={
        'labels':labels,
        'data':data,
    })

def payment_chart(request):
    labels = []
    data = []
    queryst = Payment.objects.all()[:23]

    for prod in queryst:
        labels.append(prod.payment_method)
        data.append(prod.amount_paid)

    return JsonResponse(data = {
        'labels':labels,
        'data':data,
    }
    )

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_table(request):
    if 'username' in request.session:
        value = Account.objects.all().order_by('id')
        p = Paginator(value,9)
        page = request.GET.get('page')
        values = p.get_page(page)

        return render(request,'admintable.html',{'values':values})

    return redirect(adminLogin)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def productList(request):
    if 'username' in request.session:
        values = Product.objects.all().order_by('-id')

        #setup pagination
        p = Paginator(values,3)
        page = request.GET.get('page')
        productValues =p.get_page(page)

        return render(request,'productslist.html', {'values' : values ,'productValues' : productValues})

    return redirect(adminLogin)



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def categoryList(request):
    if 'username' in request.session:
        values = Categoryies.objects.all().order_by('id')
        return render(request,'categories.html',{'values':values})
    return redirect(adminLogin)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def editproduct(request,id):
    if 'username' in request.session:
        this_product = Product.objects.get(id=id)
        values = Categoryies.objects.all()
    

        if request.method == 'POST':
        

            product_name = request.POST.get('name')
            product_description = request.POST.get('description')
            product_price = request.POST.get('price')
            product_stock = request.POST.get('stock')
            product_offer = request.POST.get('offer')
            product_image = request.POST.get('image')
            product_image1 = request.POST.get('image1')
            product_image2 = request.POST.get('image2')

            if product_name == "" or product_description == "" or product_price == "" or product_stock == ""  or product_offer == ""  or product_image == "" or product_image1 == "" or  product_image2 == "":
                if product_name == "":   
                    messages.error(request,'product name must not be empty',extra_tags='productname')
                if product_description == "":
                    messages.error(request,'product description must not be empty',extra_tags='productdescription')
                if product_image2 == "":
                    messages.error(request,'product image must not be empty',extra_tags='product_image2')
                if product_price == ""  :
                    messages.error(request,'product price must not be empty',extra_tags='product_price')
                elif float(product_price) <1:
                    messages.error(request,'product price must be valid',extra_tags='product_price')
                if product_stock == "":
                    messages.error(request,'product stock  must not be empty',extra_tags='product_stock')
                elif int(product_stock) <1:
                    messages.error(request,'product stock  must be more ',extra_tags='product_stock')
                if product_offer == ""  :
                    messages.error(request,'product offer  must not be empty',extra_tags='offerproduct')
                elif int(product_offer) >100:
                    messages.error(request,'product offer  must not be greter than 100',extra_tags='offerproduct')
                if product_image == "":
                    messages.error(request,'product image must not be empty',extra_tags='product_image0')
                if product_image1 == "":
                    messages.error(request,'product image  must not be empty',extra_tags='product_image1')

            elif float(product_price) <1 or int(product_stock) <1 or int(product_offer) >100 :
                if float(product_price) <1:
                    messages.error(request,'product price must be valid',extra_tags='product_price')
                if int(product_stock) <1:
                    messages.error(request,'product stock  must be more ',extra_tags='product_stock')
                if int(product_offer) >100:
                    messages.error(request,'product offer  must not be greter than 100',extra_tags='offerproduct')
        


            else:

                obj = Product.objects.get(id=id)

                obj.name = product_name
                obj.description = product_description
                obj.price = product_price
                obj.stock = product_stock
                obj.offerproduct = product_offer
                obj.image = product_image
                obj.image1 = product_image1
                obj.image2 = product_image2


                obj.save()
                return redirect(productList)
        return render(request,'useredit.html',{'this_product': this_product,'values':values})
    else:
        return redirect(adminLogin)

       

def deleteproduct(request,id):
    if request.method == "POST":

        print("tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
        my_product =Product.objects.get(id=id)
        my_product.delete()
        return redirect(productList)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def addproduct(request):
    if 'username' in request.session:   
        values = Categoryies.objects.all()
        if request.method == "POST":
            product_name = request.POST.get('name')
            product_description = request.POST.get('description')
            product_price = request.POST.get('price')
            product_stock = request.POST.get('stock')
            categ       = request.POST.get('category')
            product_offer =request.POST.get('offer')

            product_image = request.POST.get('image')
            product_image1 = request.POST.get('image1')
            product_image2 = request.POST.get('image2')

            if product_name == "" or product_description == "" or product_price == "" or product_stock == ""  or product_offer == ""  or product_image == "" or product_image1 == "" or  product_image2 == "":
                if product_name == "":   
                    messages.error(request,'product name must not be empty',extra_tags='productname')
                if product_description == "":
                    messages.error(request,'product description must not be empty',extra_tags='productdescription')
                if product_image2 == "":
                    messages.error(request,'product image must not be empty',extra_tags='product_image2')
                if product_price == ""  :
                    messages.error(request,'product price must not be empty',extra_tags='product_price')
                elif float(product_price) <1:
                    messages.error(request,'product price must be valid',extra_tags='product_price')
                if product_stock == "":
                    messages.error(request,'product stock  must not be empty',extra_tags='product_stock')
                elif int(product_stock) <1:
                    messages.error(request,'product stock  must be more ',extra_tags='product_stock')
                if product_offer == ""  :
                    messages.error(request,'product offer  must not be empty',extra_tags='offerproduct')
                elif int(product_offer) >100:
                    messages.error(request,'product offer  must not be greter than 100',extra_tags='offerproduct')
                if product_image == "":
                    messages.error(request,'product image must not be empty',extra_tags='product_image0')
                if product_image1 == "":
                    messages.error(request,'product image  must not be empty',extra_tags='product_image1')

            elif float(product_price) <1 or int(product_stock) <1 or int(product_offer) >100 :
                if float(product_price) <1:
                    messages.error(request,'product price must be valid',extra_tags='product_price')
                if int(product_stock) <1:
                    messages.error(request,'product stock  must be more ',extra_tags='product_stock')
                if int(product_offer) >100:
                    messages.error(request,'product offer  must not be greter than 100',extra_tags='offerproduct')
        
        


            else:
                product = Product(name = product_name ,description =product_description,price=product_price,
                stock= product_stock,image=product_image,image1=product_image1,image2=product_image2 ,offerproduct=product_offer)
                product.category  = Categoryies.objects.get(id=categ)
                product.save()
                return redirect(productList)
    
    
        return render (request,'addproduct.html',{'values':values})
    else:
        return redirect(adminLogin)



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def addcategory(request):
    if 'username' in request.session:   
    
        if request.method == "POST":
            category_name = request.POST.get('category_name')
            description = request.POST.get('description')
            offer = request.POST.get('offer')

        
            cat = Categoryies(category_name=category_name,description=description,offer=offer)
        
            cat.save()
            return redirect(categoryList)
    
    
        return render (request,'addcategory.html')
    else:
        return redirect(adminLogin)
  
def deletecategory(request,id):
    my_cat = Categoryies.objects.get(id=id)
    my_cat.delete()
    return redirect(categoryList)


def blockuser(request,id):
    user = Account.objects.get(id = id)
    if user.is_active:
        user.is_active = False
       
    else:
        user.is_active = True
       
    user.save()
    return redirect(admin_table)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def orderdisplay(request):
    if 'username' in request.session:   

        order= Orders.objects.filter(is_ordered = True).order_by('-id')
        p = Paginator(order,9)
        page = request.GET.get('page')
        orders = p.get_page(page)
    
        return render(request,'orderadmin.html',{ 'order':order,'orders':orders})
    else:
        return redirect(adminLogin)



    
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def orderstatus(request,id):
    if 'username' in request.session:   
        if request.method == "POST":
            status = request.POST.get('status')
    
            order = OrderProduct.objects.get(id = id)
            order.status = status
            order.save()

        return redirect(orderdisplay)

    else:
        return redirect(adminLogin)

def offerstatus(request,id):
    if request.method == "POST":
        status = request.POST.get('offer')
    
        categ = Categoryies.objects.get(id = id)
        categ.offer = status
        categ.save()

    return redirect(categoryList)

def offerstatusedit(request,id):
    if request.method == "POST":
        status = request.POST.get('offer')
    
        categ = Categoryies.objects.get(id = id)
        categ.offer = status
        categ.save()

    return redirect(categoryoffermanage)

def  searchprod(request):
    try:
        q = request.GET['search']
        
        data = Product.objects.all()
        datas = []
    
        for i in data :
            datas.append(i.name)

        for i in datas:
           if q.lower() in i.lower():
               searched = Product.objects.filter(name = i)
               

        print(searched)

        return render(request,'productslists.html', {'productValues' : searched})
    except:
        return render(request,'noproduct.html')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def orderdetailsadmin(request,id):
    if 'username' in request.session:   

        orderprod = OrderProduct.objects.filter(order = id).order_by('-id')
        return render (request,'orderdetailsadmin.html',{'orderprod':orderprod} )

    else:
        return redirect(adminLogin)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def couponlist(request):
    if 'username' in request.session:   

        coupons = Coupon.objects.all().order_by('-id')
        return render(request,'coupons.html',{'coupons':coupons})

    else:
        return redirect(adminLogin)

def disableorenablecoupon(request, id):
    coupon = Coupon.objects.get(id = id)
    if coupon.is_active :
        coupon.is_active = False
    else :
        coupon.is_active = True
    coupon.save()
    return redirect(couponlist)

def couponadd(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        if coupon_code == '':
            messages.error(request,'coupon must not be empty',extra_tags='coupon')
        if discount == '':
            messages.error(request,'Discount mustnot be empty',extra_tags='discount')

        elif Coupon.objects.filter(discount =discount,coupon_code =coupon_code).exists() :
            messages.error(request,'coupon code already exist',extra_tags='coupon')
            messages.error(request,'Discount already exist',extra_tags='discount')

        elif Coupon.objects.filter(discount =discount).exists() :
            messages.error(request,'Discount already exist',extra_tags='discount')

        elif Coupon.objects.filter(coupon_code =coupon_code).exists() :
            messages.error(request,'coupon code already exist',extra_tags='coupon')

        elif int(discount) < 100 or int(discount) > 2000:
            messages.error(request,'Discount must be greater than 100',extra_tags='discount')
            
        else:
            newcoupon = Coupon(coupon_code=coupon_code,discount=discount)
            newcoupon.save()
            return redirect(couponlist)
    return render (request,"couponadd.html")

    
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def salesreport(request):
    if 'username' in request.session:   
    
    
        salesreport = Orders.objects.filter(is_ordered = True).order_by('-id')
    
        if request.method  == 'POST':
            search = request.POST["salesreport_search"]
            salesreports = Orders.objects.filter(orderid__contains = search)
            context = {
                'salesreport':salesreports
            }
            return render (request,"salesreport.html",context)
   
        context = {
                'salesreport':salesreport
            }
        return render (request,"salesreport.html",context)
    else:
        return redirect(adminLogin)

def date_range(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        if len(fromdate)>0 and len(todate)> 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]

            salesreport = Orders.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]) ,is_ordered =True)

            context = {
                'salesreport':salesreport,
            }

            return render(request,'sales_report_search.html',context)

        else:
            salesreport = Orders.objects.all()
            context = {
                'salesreport': salesreport ,

             }
            


    return render (request,"salesreport.html",context)
        


def monthly_report(request,date):
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,28]

    salesreport = Orders.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]),is_ordered =True)
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'sales_report_search.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'sales_report_search.html')

def yearly_report(request,date):
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]

    salesreport = Orders.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]),is_ordered =True)
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'sales_report_search.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'sales_report_search.html')


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def adminbanner(request):
    if 'username' in request.session:   

        banner = Banner.objects.all().order_by('id')
        return render(request,'adminbanner.html',{'banner' :banner})
    else:
        return redirect(adminLogin)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def addbanner(request):
    if 'username' in request.session:   

        if request.method == "POST":
            banner = request.POST.get('banner')
            title = request.POST.get('title')
            description = request.POST.get('description')

            newbanner = Banner(banner=banner,title=title,description=description)
            newbanner.save()
            return redirect(adminbanner)


        return render(request,'addbanner.html')
    else:
        return redirect(adminLogin)

def deletebanner(request,id):
    banner = Banner.objects.get(id =id)
    banner.delete()
    return redirect(adminbanner)


    
def selectbanner(request,id):

    banner = Banner.objects.get(id =id)
    if banner.is_selected == True:
        banner.is_selected = False
    else :
        banner.is_selected = True
    banner.save()
    return redirect(adminbanner)


def offermanage(request):
    return render(request,'offermanage.html')


def productoffermanage(request):
    if 'username' in request.session:
        values = Product.objects.all().order_by('-id')

        #setup pagination
        p = Paginator(values,3)
        page = request.GET.get('page')
        productValues =p.get_page(page)

        return render(request,'productoffermanage.html', {'values' : values ,'productValues' : productValues})

    return redirect(adminLogin)
    

def categoryoffermanage(request):
    # if 'username' in request.session:

    
    values = Categoryies.objects.all().order_by('-id')
        



    
    return render(request,'categoryoffermanage.html',{'values':values})

def disablecatoffer(request, id):
    cat = Categoryies.objects.get(id = id)
    if cat.offerstatus == True:
        

        cat.offerstatus = False
        
    else :
        cat.offerstatus = True
    cat.save()
    return redirect(categoryoffermanage)

def disableprodoffer(request, id):
    pro = Product.objects.get(id = id)
    if pro.offerstatuspro == True:
        

        pro.offerstatuspro = False
        
    else :
        pro.offerstatuspro = True
    pro.save()
    return redirect(productoffermanage)



def offerstatuseditproduct(request,id):
    if request.method == "POST":
        status = request.POST.get('offer')
    
        prod = Product.objects.get(id = id)
        prod.offerproduct = status
        prod.save()

    return redirect(productoffermanage)
