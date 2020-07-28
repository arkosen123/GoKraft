
from django.urls import path
from itemAndCart.api.views import (

        api_add_to_cart,
        api_remove_from_cart,    
)


app_name = 'itemAndCart'


urlpatterns=[


    #################################
    #the order request
    #################################
    path('add-to-cart/<slug>', api_add_to_cart, name = 'add_to_cart'),
    path('remove-from-cart/<slug>',api_remove_from_cart, name='remove_from_cart'),
]