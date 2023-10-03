from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Authentication
    path('login/', views.user_login_or_sign_up, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Navigation
    path('', views.gallery, name='gallery'),
    path('my-posted-items/', views.my_posted_items, name='my-posted-items'),
    path('product-details/<str:pk>/', views.product_details, name='product-details'),
    
    # Auction Product CRUD
    path('create-auction-product/', views.create_auction_product, name='create-auction-product'),
    path('update-auction-product/<str:pk>/', views.update_auction_product, name='update-auction-product'),
    path('delete-auction-product/<str:pk>/', views.delete_auction_product, name='delete-auction-product'),

    # Bidder CRUD
    path('add-bid/<str:pk>/', views.add_bid, name='add-bid'),
    path('update-bid/<str:pk>/', views.update_bid, name='update-bid'),
    path('delete-bid/<str:pk>/', views.delete_bid, name='delete-bid'),

    # Admin Only
    path('dashboard/', views.view_dashboard, name='dashboard'),

]

