from django.db import models
from apps.Users.models import User
from apps.Products.models import Product
import uuid


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='CartProduct')

    class Meta:
        db_table = 'cart'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_product'
        unique_together = ('cart', 'product') 