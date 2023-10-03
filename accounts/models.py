import django
from django.db import models
from django.contrib.auth.models import User
import os
import uuid
import datetime

# https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
def get_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images', filename)
#create signup page
# Create your models here.
class AuctionProduct(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=200, null=True)
    product_description = models.TextField(null=True)
    product_photo = models.ImageField(null=True, blank=True, upload_to=get_file_name)
    minimum_bid_price = models.DecimalField(max_digits=12, decimal_places=2)
    auction_end_date_time = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    # @property
    # def auction_ended(self):
    #     return datetime.datetime.now() > self.auction_end_date_time


    def __str__(self):
        return self.product_name

class Bidder(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_product_id = models.ForeignKey(AuctionProduct, on_delete=models.CASCADE, default=None)
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} - {self.auction_product_id}"
    
# class Signup(models.Model):
#     name=models.CharField(max_length=50)
#     passw=models.CharField(max_length=50)
#     rpass=models.CharField(max_length=50)
#     email=models.EmailField(max_length=70)

#     def __str__(self):
#         return self.name+  " "+ self.email


    
