
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):

    #code to create a normal user

    def create_user(self,first_name,last_name,username,email,phone_number,password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            
            first_name   =   first_name,
            last_name    =   last_name,
            username     =   username,
            email        =   self.normalize_email(email),
            phone_number =   phone_number,

        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user

    #code to create superuser

    def create_superuser(self,first_name,last_name,username,email,phone_number,password):
        user    =   self.create_user(
            email        =   self.normalize_email(email),
            username     =   username,
            first_name   =   first_name,
            last_name    =   last_name,
            password = password,
            phone_number =   phone_number
            
            
        )
        user.is_admin       =   True
        user.is_active      =   True
        user.is_staff       =   True
        user.is_superuser   =   True   #user.is_superadmin  = True     in jakson code
        user.save(using=self._db)
        return user
         
    


class Account(AbstractBaseUser):
    first_name      =   models.CharField(max_length=50 ,null=True)
    last_name       =   models.CharField(max_length=50 ,null=True)
    username        =   models.CharField(max_length=50 , unique=True)
    email           =   models.EmailField(max_length=100, unique=True)
    phone_number    =   models.CharField(max_length=50, unique=True,null=True)
    wallet          =   models.FloatField(null=True)
    

    #required
    date_joined     =   models.DateTimeField(auto_now_add=True)
    last_login      =   models.DateTimeField(auto_now_add=True)
    is_admin        =   models.BooleanField(default=False)
    is_staff        =   models.BooleanField(default=False)
    is_active       =   models.BooleanField(default=True)
    is_superuser    =   models.BooleanField(default=False)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name','phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Address(models.Model):
    firstname      =   models.CharField(max_length=50 ,null=True)
    lastname       =   models.CharField(max_length=50 ,null=True)
    phonenumber    =   models.CharField(max_length=50 ,null=True)
    housename      =   models.CharField(max_length=50 ,null=True)
    town           =   models.CharField(max_length=50 ,null=True) 
    locality       =   models.CharField(max_length=50 ,null=True) 
    city           =   models.CharField(max_length=50 ,null=True) 
    state          =   models.CharField(max_length=50 ,null=True) 
    pincode        =   models.CharField(max_length=50 ,null=True)
    user           =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return self.firstname

class trial(models.Model):
    first_name      =   models.CharField(max_length=50 ,null=True)
    last_name       =   models.CharField(max_length=50 ,null=True)
    username        =   models.CharField(max_length=50 , unique=True)
    email           =   models.EmailField(max_length=100, unique=True)
    phone_number    =   models.CharField(max_length=50, unique=True,null=True)
    password        =   models.CharField(max_length=50, unique=True,null=True)
    