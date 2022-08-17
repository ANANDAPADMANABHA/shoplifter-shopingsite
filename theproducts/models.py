from ast import Return
from itertools import product
from django.db import models

# Create your models here.






class Categoryies(models.Model):
    category_name = models.CharField( max_length=50)
    description = models.CharField(max_length=200)
    offer = models.IntegerField( null=True)
    offerstatus = models.BooleanField(default=True)


    def __str__(self):
        return self.category_name 


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    stock = models.IntegerField()
    category  = models.ForeignKey(Categoryies, on_delete=models.CASCADE, null=True, blank=True)
    offerproduct = models.IntegerField(null=True)
    image = models.CharField(max_length=2500)
    image1 = models.CharField(max_length=2500, null=True)
    image2 = models.CharField(max_length=2500, null=True)
    offerstatuspro = models.BooleanField(default=True)



    def __str__(self):
        return self.name
    def offer_price(self):

        if self.category.offerstatus == True and self.offerstatuspro == True:
            if self.offerproduct:
                if self.category.offer > self.offerproduct:
                    return self.price - self.price *(self.category.offer/100)

                else:
                    return self.price - self.price*(self.offerproduct/100)
                
            else:
                return self.price - self.price *(self.category.offer/100)

        elif self.category.offerstatus == False and self.offerstatuspro == True:
            
            return self.price - self.price *(self.offerproduct/100)

        elif self.category.offerstatus == True and self.offerstatuspro == False:
            return self.price - self.price *(self.category.offer/100)

        else:
            return self.price
            
    def max_offer(self):
      
        if self.category.offerstatus == True and self.offerstatuspro == True:
            if self.offerproduct:
                if self.category.offer > self.offerproduct:
                    return self.category.offer
                else:
                    return self.offerproduct
                
            else:
                return self.category.offer

        elif self.category.offerstatus == False and self.offerstatuspro == True:
            return self.offerproduct

        elif self.category.offerstatus == True and self.offerstatuspro == False:
            return self.category.offer

        else:
            return "No offer"


