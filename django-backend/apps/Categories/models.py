from django.db import models
import uuid


class CatTypes(models.TextChoices):
    SHIRT = "SHIRT", "Shirt"
    PANTS = "PANTS", "Pants"
    SHOES = "SHOES", "Shoes"
    ACCESSORIES = "ACCESSORIES", "Accessories"
    ELECTRONICS = "ELECTRONICS", "Electronics"
    BOOKS = "BOOKS", "Books"
    SPORTS = "SPORTS", "Sports"
    BEAUTY = "BEAUTY", "Beauty"
    HEALTH = "HEALTH", "Health"
    HOME = "HOME", "Home"
    TOYS = "TOYS", "Toys"
    FOOD = "FOOD", "Food"


class Category(models.Model):
    cat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cat_name = models.CharField(
        max_length=20,
        choices=CatTypes.choices,
        default=CatTypes.SHIRT,
        unique=True
    )

    class Meta:
        db_table = 'categories'


class CategoryProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_products'
        unique_together = ('category', 'product') 