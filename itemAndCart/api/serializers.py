from rest_framework import serializers
from itemAndCart.models import Item,Order,OrderItem


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = ['title','category','price','discounted_price','description']


class OrderItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = ['quantity']
		#title = item title to be added to cart, not necessary as we can get it from slug
		#quantity = no of items added to cart
