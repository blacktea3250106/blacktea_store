from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Capacity(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product-images",null=True)
    price = models.IntegerField(default=0)
    formatted_price = models.CharField(max_length=100, editable=False)
    content = models.TextField(validators=[MinLengthValidator(10)])
    time = models.CharField(max_length=10)
    style_color = models.ManyToManyField(Color)
    style_capacity = models.ManyToManyField(Capacity)
    slug = models.SlugField(unique=True, default="", null=False)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product", args=[self.slug])
    
    def format_price(self):
        self.formatted_price = "NT$ {:,}".format(self.price)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.format_price()
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="cart")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart")
    style_color = models.ManyToManyField(Color)
    style_capacity = models.ManyToManyField(Capacity)
    volume = models.IntegerField(default=1, validators=[MaxValueValidator(9999)])
    total = models.IntegerField(default=0,editable=False)
    formatted_price = models.CharField(max_length=100,editable=False,default="")

    def calc_total(self):
        self.total = self.product.price * self.volume

    def format_total(self):
        self.formatted_price = "NT$ {:,}".format(self.total)
    
    def save(self, *args, **kwargs):
        self.calc_total()
        self.format_total()
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="comments") # on_delete=models.SET_NULL -> 刪掉user不會刪除Comment全部留言
    text = models.TextField(max_length=400)
    star_num = models.IntegerField(default=-1, blank=True, null=True)
    date = models.DateField(auto_now=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments")
    # on_delete=models.CASCADE -> 刪掉Product也會連帶刪除Comment留言

    def __str__(self):
        return self.text
    

