from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from itemAndCart.models import Item
from itemAndCart.api.serializers import ItemSerializer


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
    try:
        item_object = Item.objects.get(slug = slug)
        temp = request.data['title']
        temp = temp.replace(' ','-')
        item_object.slug = temp
    except Item.doesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = {}
        serializer = ItemSerializer(item_object, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data = data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE',])
def api_delete_item_details(request, slug):
    try:
        item_object = Item.object.get(slug = slug)
    except Item.doesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        data = {}
        opetation = item_object.delete()
        if opetation:
            data["success"] = "Delete successful"
        else:
            data["faliure"] = "Delete failed"


        return Response(data = data)



@api_view(['POST',])
def api_create_item_details(request):
    
    item_object = Item(slug = request.data['title'])
    if request.method == 'POST':
        serializer = ItemSerializer(item_object, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

