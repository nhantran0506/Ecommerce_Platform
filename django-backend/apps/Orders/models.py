from django.db import models
from apps.Users.models import User
from apps.Products.models import Product
import uuid


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem')

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    class OrderStatus(models.TextChoices):
        PROCESSING = "PROCESSING", "Processing"
        TRANSPORTING = "TRANSPORTING", "Transporting"
        PRODUCT_ACCEPTED = "PRODUCT_ACCEPTED", "Product Accepted"
        PRODUCT_PREPARING = "PRODUCT_PREPARING", "Product Preparing"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )
    order_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    recieved_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'order_items'
        unique_together = ('order', 'product') 