from django.urls import path

from itemAndCart.api.views import (
                    api_get_item_details , 
                    api_update_item_details,
                    api_delete_item_details,
                    api_create_item_details,

                    api_add_to_cart,
                    api_remove_from_cart,
                    )
    

app_name = 'itemAndCart'


urlpatterns = [
    
    path('<slug>/', api_get_item_details, name = 'get_item_details'),#must be a get req
    path('<slug>/update', api_update_item_details, name = 'update_item_details'),#must be a put req
    path('<slug>/delete', api_delete_item_details, name = 'delete_item_details'),# must be a delete req
    path('create', api_create_item_details, name = 'create_item_details'),



    ##########################
    #now all the order request
    ##########################

    path('add-to-cart/<slug>', api_add_to_cart, name = 'add_to_cart'),
    path('remove-from-cart/<slug>',api_remove_from__cart, name='remove_from__cart'),
]
