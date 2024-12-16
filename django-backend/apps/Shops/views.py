from rest_framework import generics
from .models import Shop, ShopRating
from .serializers import ShopSerializer, ShopRatingSerializer

class ShopListView(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'shop_id'

class ShopProductsView(generics.ListAPIView):
    serializer_class = ShopSerializer
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Shop.objects.filter(shop_id=shop_id)

class ShopRatingsView(generics.ListCreateAPIView):
    serializer_class = ShopRatingSerializer
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return ShopRating.objects.filter(shop_id=shop_id)