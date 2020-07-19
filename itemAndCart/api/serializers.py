from rest_framework import serializers
from itemAndCart.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['title','category','price','discounted_price','description']