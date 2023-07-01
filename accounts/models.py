from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class MyAccountmanager(BaseUserManager):
    def create_user( self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email        = self.normalize_email(email),
            username     = username,
            first_name   = first_name,
            last_name    = last_name, 
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email        = self.normalize_email(email),
            password     = password,
            username     = username,
            first_name   = first_name,
            last_name    = last_name,
        )
        
        user.is_active     = True
        user.is_admin      = True
        user.is_staff      = True
        user.is_superadmin = True 
        user.save(using = self._db)
 
class User(AbstractBaseUser,PermissionsMixin):
    VENDOR  = 1
    CUSTOMER    = 2

    
    ROLE_CHOICE = (
        (VENDOR,   'VENDOR'),
        (CUSTOMER,     'CUSTOMER'),
    )
    
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    email         = models.EmailField(max_length=100, unique=True)
    username      = models.CharField(max_length=50, unique=True)
    phone_number  = models.CharField(max_length=12, blank=True)
    role          = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null = True)
    
    SearchableFields   = ['first_name', 'email', 'phone_number', 'role']
    
    
    date_joined    = models.DateTimeField(auto_now_add=True)
    last_login     = models.DateTimeField(auto_now_add=True)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=False)
    is_admin       = models.BooleanField(default=False)
    is_superadmin  = models.BooleanField(default=False)
    
    
    USERNAME_FIELD  =  'email'
    REQUIRED_FIELDS =  ['username', 'first_name', 'last_name' ]
    
    objects = MyAccountmanager()
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
   
    
    def get_role(self):
        if self.role == 1:
            user_role = 'VENDOR'
        elif self.role == 2:
            user_role = 'CUSTOMER'
        return user_role
    
    

class UserProfile(models.Model):
    user               = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    profile_picture    = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photos       = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1     = models.CharField(max_length=100, blank=True, null=True)
    address_line_2     = models.CharField(max_length=100, blank=True, null=True)
    country            = models.CharField(max_length=50, blank=True, null=True)
    state              = models.CharField(max_length=50, blank=True, null=True)
    city               = models.CharField(max_length=50, blank=True, null=True)
    pincode           = models.CharField(max_length=6, blank=True, null=True)
    latitude           = models.CharField(max_length=20, blank=True, null=True)
    longitude          = models.CharField(max_length=20, blank=True, null=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    modified_at        = models.DateTimeField(auto_now=True)
    SearchableFields   = ['user', 'country','city','state','pincode']
    
    def save(self, *args, **kwargs):
        self.user.first_name = self.user.first_name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email