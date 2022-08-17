from django.db import models
from accounts.models import Account
from theproducts.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE)
    cart        =   models.ForeignKey(Cart,on_delete=models.CASCADE ,null=True)
    quantity    =   models.IntegerField()
    cartprice = models.FloatField(null = True)
    is_active   =   models.BooleanField(default=True)
    buy_now =   models.BooleanField(default=False)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10,blank=True)
    discount    = models.FloatField()
    is_active   =   models.BooleanField(default=True)

class UsedCoupon(models.Model):
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    coupon        =   models.ForeignKey(Coupon,on_delete=models.CASCADE, null=True)




