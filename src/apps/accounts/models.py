from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from typing import ClassVar

# Create your models here.

class RoleChoices(models.TextChoices):
    USER = 'user', 'User'
    MEMBER = 'member', 'Member'
    ADMIN = 'admin', 'Admin'


class UserAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, city, country, password=None, role=RoleChoices.USER):
         
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
            role = role,
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
            role = RoleChoices.ADMIN,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):

    profile_picture = models.ImageField(upload_to='profile/img', null=True, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.USER)

    birth_date = models.DateField(null=True, blank=True)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(blank=True, null=True)
    
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'city', 'country']

    objects: ClassVar[UserAccountManager] = UserAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_user_role(self):
        return self.role == RoleChoices.USER

    @property
    def is_member(self):
        return self.role in [RoleChoices.MEMBER, RoleChoices.ADMIN] or self.is_superuser or self.is_staff

    @property
    def is_admin_role(self):
        return self.role == RoleChoices.ADMIN or self.is_superuser or self.is_staff

    def save(self, *args, **kwargs):
        if self.role == RoleChoices.ADMIN:
            self.is_staff = True
            self.is_admin = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_admin = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



