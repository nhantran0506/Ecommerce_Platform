from rest_framework import serializers
from .models import Shop, ShopRating

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class ShopRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopRating
        fields = '__all__'