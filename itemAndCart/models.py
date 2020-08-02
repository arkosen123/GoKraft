

# Create your models here.
from django.db import models
from django.conf import settings 
from django.shortcuts import reverse

from accounts.models import Account


# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length = 100, null = False, blank = False)
    category = models.CharField(max_length = 100, null = False, blank = False)
    description = models.TextField()
    price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    picture = models.ImageField(blank = True, null = True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("itemAndCart:item", kwargs={"slug": self.slug})
    

class OrderItem(models.Model):
    #contain the ordered items
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    #user_id = user.pk
    items =  models.ManyToManyField(OrderItem)
    start_dates = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False) #to ensure the order has not completed

    def __str__(self):
        return self.user.username