
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'suv'),(2,'sedan'),(3,'hatchback'))
    name=models.CharField(max_length=50,verbose_name='product_name')
    price=models.FloatField()
    location=models.CharField(max_length=80,verbose_name='location')
    category=models.IntegerField(verbose_name='categories',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='available')
    pimage=models.ImageField(upload_to='image')
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)