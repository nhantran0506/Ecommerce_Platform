from django.db import models
from django.core.validators import MinValueValidator
from apps.Users.models import User
import uuid


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    create_at_datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    avg_stars = models.FloatField(default=0.0, null=True)
    total_ratings = models.IntegerField(default=0, null=True)
    total_sales = models.IntegerField(default=0, null=True)
    inventory = models.IntegerField(default=0, null=True)
    categories = models.ManyToManyField('categories.Category', through='categories.CategoryProduct')

    class Meta:
        db_table = 'products'


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_ratings')
    rating_stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)

    class Meta:
        db_table = 'product_rating'
        unique_together = ('product', 'user')


class ImageProduct(models.Model):
    image_url = models.CharField(max_length=255, unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_product')

    class Meta:
        db_table = 'image_products' 