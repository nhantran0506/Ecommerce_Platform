from django.db import models
from apps.Users.models import User
from apps.Products.models import Product
import uuid


class UserInterest(models.Model):
    class InterestScore(models.IntegerChoices):
        VIEW = 1, "View"
        CART = 3, "Cart"
        BUY = 5, "Buy"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_interest')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='interest')
    score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_interest'
        unique_together = ('user', 'product') 