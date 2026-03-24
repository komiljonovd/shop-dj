from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, full_name, phone_number, password=None, **extra_fields):
        if not full_name:
            raise ValueError('Full name is required')
        if not phone_number:
            raise ValueError('Phone number is required')

        user = self.model(
            full_name=full_name,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        return self.create_user(full_name, phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = None

    full_name = models.CharField(max_length=128,verbose_name='Ф.И.О',unique=True)
    phone_number = models.CharField(max_length=128,verbose_name='Телефон номер',unique=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Дата изменения')
    
    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.full_name