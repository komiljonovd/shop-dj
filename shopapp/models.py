from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()


class OrderStatus(models.TextChoices):
    in_progress = 'in_progress',_('В процессе')
    delivered = 'delivered',_('Доставлено')


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64,verbose_name='Название')
    price = models.FloatField(verbose_name='Цена')
    image = models.ImageField(verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Дата изменения')

    class Meta:
        db_table = 'Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Пользователь')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Продукт')
    quantity = models.PositiveIntegerField(null=True,blank=True,default=1,verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    class Meta:
        db_table = 'Cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f'{self.user.get_full_name}' | f'{self.product.name}'
    
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Пользователь')
    total = models.FloatField(verbose_name='Общая сумма')
    status = models.CharField(max_length=32,choices=OrderStatus,default=OrderStatus.in_progress,verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    class Meta:
        db_table = 'Order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.user.get_full_name}' | f'{self.status}'