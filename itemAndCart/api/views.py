from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone


from itemAndCart.models import Item,Order,OrderItem
from itemAndCart.api.serializers import (
    ItemSerializer,
    OrderItemSerializer,
    )


@api_view(['GET',])
def api_get_item_details(request, slug):
    try:
        item = Item.objects.get(slug = slug)
    except Item.doesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)


@api_view(['PUT',])
def api_update_item_details(request, slug):
    data = {}
    try:
        item_object = Item.objects.get(slug = slug)
        temp = request.data['title']
        temp = temp.replace(' ','-')
        item_object.slug = temp
    except Item.doesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    

    if item_object.seller != request.user:
        data['faliure'] = 'User is not the seller of this item'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        
        serializer = ItemSerializer(item_object, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data = data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE',])
def api_delete_item_details(request, slug):
    data = {}
    try:
        item_object = Item.object.get(slug = slug)
    except Item.doesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)



    if item_object.seller != request.user:
        data['faliure'] = 'User is not the seller of this item'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        opetation = item_object.delete()
        if opetation:
            data["success"] = "Delete successful"
        else:
            data["faliure"] = "Delete failed"


        return Response(data = data)



@api_view(['POST',])
def api_create_item_details(request):
    
    temp = request.data['title']
    temp = temp.replace(' ','-')
    item_object = Item(slug = temp)
    item_object.seller = request.user
    if request.method == 'POST':
        serializer = ItemSerializer(item_object, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)




###########################################################
#Order handling
############################################################

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)


    if item == None:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    
    data = {}
    if int(request.data['quantity']) < 0:
        data['faliure'] = 'Item number cannot be less than zero'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                user = request.user,
                                                ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)



    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += int(request.data['quantity'])
            order_item.save()
            data['success'] = 'Cart updated successfully.'

        else:
            order_item.quantity = int(request.data['quantity'])
            order_item.save()
            order.items.add(order_item)
            data['success'] = 'Item added to cart successfully.'

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order_item.quantity = int(request.data['quantity'])
        order_item.save()
        order.items.add(order_item)
        data['success'] = 'Item added to cart successfully.'

    data['user'] = request.user.email
    data['quantity'] = order_item.__str__()
    

    return Response(data = data, status = status.HTTP_200_OK)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_remove_from_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    if item == None:
        return Response(status= status.HTTP_400_BAD_REQUEST)

    data={}
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(item=item,user = request.user, ordered = False)[0]
            order.items.remove(order_item)
            order_item.delete()
            data['delete'] = 'Order deleted successfully.'
        else:
            data['delete']="User doesn't contain the order."
    else:
        data['delete']="User doesn't have any order."

    return Response(data = data, status = status.HTTP_200_OK)

