from django.db import models
from accounts.models import Account, Address
from cartapp.models import Cart, CartItem
from theproducts.models import Product

# Create your models here.
class Payment(models.Model):


    user =  models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=100,null=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.payment_method

class Orders(models.Model):

    STATUS = (
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out_for_delivery','Out_for_delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )

    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    address     =   models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
    ordertotal  =   models.FloatField(max_length=50 ,null=True)
    orderid     =   models.CharField(max_length=100,null=True)
    date        =   models.DateField(null=True,auto_now_add=True)
    payment     =   models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    status      =   models.CharField(max_length=30, choices=STATUS, default='Confirmed')
    is_ordered  =   models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name


class OrderProduct(models.Model):
    STATUS = (
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out_for_delivery','Out_for_delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    
    order       =   models.ForeignKey(Orders,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    quantity    =   models.IntegerField(null=True)
    price       =   models.FloatField(max_length=200,null=True)
    status      =   models.CharField(max_length=30, choices=STATUS, default='Confirmed')


    def sub_total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product.name
