from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, city, country, password=None):
         
        if not username:
            raise ValueError('User must have an unique username')
        
        if not email:
            raise ValueError('User must have an unique email address')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            city = city,
            country = country,
        )
         
        user.is_active = True 

        user.set_password(password)
        user.save(using=self._db)
        return user
    

     
     
    def create_superuser(self, first_name, last_name, username, email, city, country, password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            city = city,
            country = country,
            password = password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)
        return user

         





class UserAccount(AbstractBaseUser):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    
    birth_date = models.DateField(null=True, blank=True)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)


    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'city', 'country']

    objects = UserAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
