from django.contrib import admin
from .models import AuctionProduct, Bidder

# Register your models here.
admin.site.register(AuctionProduct)
admin.site.register(Bidder)
# admin.site.register(Signup)
