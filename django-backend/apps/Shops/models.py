from django.db import models
from apps.Users.models import User
from apps.Products.models import Product
import uuid


class Shop(models.Model):
    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop_name = models.CharField(max_length=255)
    shop_address = models.CharField(max_length=255)
    shop_phone_number = models.CharField(max_length=20, unique=True)
    shop_bio = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    avg_stars = models.FloatField(default=0.0, null=True)
    total_ratings = models.IntegerField(default=0, null=True)
    products = models.ManyToManyField(Product, through='ShopProduct')

    class Meta:
        db_table = 'shop'


class ShopProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shop_products')

    class Meta:
        db_table = 'shop_products'
        unique_together = ('shop', 'product')


class ShopRating(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_ratings')
    rating_stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)

    class Meta:
        db_table = 'shop_rating'
        unique_together = ('shop', 'user') 