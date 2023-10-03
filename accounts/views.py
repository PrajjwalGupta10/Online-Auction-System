import datetime
from django.db.models.aggregates import Count, Max, Sum
import pytz
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, AuctionProductForm, BidderForm
from .models import AuctionProduct, Bidder
from accounts import forms
from .decorators import unauthenticated_user
# from accounts.models import Signup
# Create your views here.

#---Authentication---##########################################################
# def signup(request):
#     if request.method=="POST":
#         name=request.POST['name']
#         passw=request.POST['passw']
#         rpass=request.POST['rpass']
#         email=request.POST['email']
#         v=Signup(name=name,passw=passw,rpass=rpass,email=email)
#         v.save()
#         print('succesfull')
#         return (request, 'accounts/signin_signup.html')
@unauthenticated_user
def user_login_or_sign_up(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        # registration
        if request.POST.get('submit') == 'Sign Up':
            form = UserRegistrationForm(request.POST)
            # print(form.username)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                # print(username)
                # print(password)
                form.save()
                messages.success(request, f'Account was created for {username}')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('gallery')

        # login
        elif request.POST.get('submit') == 'Sign In':
            username = request.POST.get('username')
            password = request.POST.get('password')
           
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('gallery')
            else:
                # meaning user doesn't exist
                messages.info(request, 'Username Or Password incorrect!')

    context = {'form': form}
    return render(request, 'accounts/signin_signup.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')





################################################################################



#---Internal App Routes---##########################################################

@login_required(login_url='login')
def gallery(request):
    auction_products = AuctionProduct.objects.all()
    context = {'products': auction_products, 'prompt': 'Auction Gallery'}
    return render(request, 'accounts/gallery.html', context)

@login_required(login_url='login')
def my_posted_items(request):
    uid = request.user.id
    my_products = AuctionProduct.objects.filter(user_id=uid).order_by('-date_created')
    context = {'products': my_products, 'prompt': 'My Auction Items'}
    return render(request, 'accounts/gallery.html', context)


@login_required(login_url='login')
def product_details(request, pk):
    product = AuctionProduct.objects.get(id=pk)
    bidders = Bidder.objects.filter(auction_product_id=pk).order_by('-bid_amount')
    winner = bidders.first
    current_user_as_bidder = Bidder.objects.filter(auction_product_id=pk, bidder=request.user)
    tz = pytz.timezone('Asia/Dhaka')
    today =  datetime.datetime.now(tz=tz)
    context = {
        'product': product,
        'bidders': bidders,
        'current_user_as_bidder': current_user_as_bidder,
        'today': today,
        'winner': winner,
    }
    return render(request, 'accounts/product_details.html', context)

##############################################################################



#---Create Routes---############################################################

@login_required(login_url='login')
def create_auction_product(request):
    product_instance = AuctionProduct(user_id=request.user)
    form = AuctionProductForm(instance=product_instance)

    if request.method == 'POST':
        form = AuctionProductForm(request.POST, request.FILES, instance=product_instance)
        if form.is_valid():
            form.save()
            return redirect('my-posted-items')

    context = {'form': form}
    return render(request, 'accounts/auction_product_form.html', context)


@login_required(login_url='login')
def add_bid(request, pk):
    product = AuctionProduct.objects.get(id=pk)
    initial = {
        'bidder': request.user,
        'auction_product_id': product,
        'bid_amount': product.minimum_bid_price
    }
    bidder_form = BidderForm(initial=initial)
    if request.method == 'POST':
        bidder_form = BidderForm(request.POST, initial=initial)
        if bidder_form.is_valid():
            bidder_form.save()
            return HttpResponseRedirect(reverse('product-details', args=[product.id]))
    context = {'form': bidder_form, 'product': product}
    return render(request, 'accounts/add_bid.html', context)

##############################################################################



#---Update and Delete Routes---############################################################

@login_required(login_url='login')
def update_auction_product(request, pk):
    product = AuctionProduct.objects.get(id=pk)
    form = AuctionProductForm(instance=product)
    if request.method == 'POST':
        form = AuctionProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product-details', args=[product.id]))
    context = {'pk': pk, 'form': form}
    return render(request, 'accounts/auction_product_form.html', context)

@login_required(login_url='login')
def delete_auction_product(request, pk):
    product = AuctionProduct.objects.get(id=pk)
    prompt_content = f'"{product.product_name}"'
    if request.method == 'POST':
        product.delete()
        return redirect('my-posted-items')
    context = {'pk': pk, 'product': product, 'presentation': prompt_content}
    return render(request, 'accounts/delete_page.html', context)

@login_required(login_url='login')
def update_bid(request, pk):
    product = AuctionProduct.objects.get(id=pk)
    bid_person = Bidder.objects.get(bidder=request.user, auction_product_id=product)
    form = BidderForm(instance=bid_person)
    if request.method == 'POST':
        form = BidderForm(request.POST, instance=bid_person)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product-details', args=[product.id]))
    context = {'pk': pk, 'form': form}
    return render(request, 'accounts/add_bid.html', context)

@login_required(login_url='login')
def delete_bid(request, pk):
    product = AuctionProduct.objects.get(id=pk)
    bid_person = Bidder.objects.get(bidder=request.user, auction_product_id=product)
    prompt_content = f'Your Bid on "{product.product_name}"'
    if request.method == 'POST':
        bid_person.delete()
        return HttpResponseRedirect(reverse('product-details', args=[product.id]))

    context = {'pk': pk, 'product': product, 'presentation': prompt_content}
    return render(request, 'accounts/delete_page.html', context)

##############################################################################



#---Admin Only---############################################################

def view_dashboard(request):
    "https://youtu.be/Gp0GFYHHPsM"
    products = AuctionProduct.objects.all()
    creation_dates = [date['date_created'].isoformat() for date in products.values('date_created')]
    bidders = Bidder.objects.all()
    tz = pytz.timezone('Asia/Dhaka')
    today =  datetime.datetime.now(tz=tz)
    live_auctions = products.filter(auction_end_date_time__gte=today)
    ended_auctions = products.filter(auction_end_date_time__lt=today)
    number_of_live_auctions = live_auctions.count()
    number_of_auctions_completed = ended_auctions.count()

    # Querrying the highest bid amount per products
    sum_of_products_worth_by_group = (
        Bidder
            .objects
            .values('auction_product_id')
            .annotate(max_bid=Max('bid_amount'))
            .order_by()
    )

    # Querry of worth stats
    sum_of_all_products_worth = (
        sum_of_products_worth_by_group
            .aggregate(Sum('max_bid'))['max_bid__sum']
    ) or '---'
    sum_of_live_products_worth = (
        sum_of_products_worth_by_group
            .filter(auction_product_id__auction_end_date_time__gte=today)
            .aggregate(Sum('max_bid'))['max_bid__sum']
    ) or '---'
    sum_of_completed_products_worth = (
        sum_of_products_worth_by_group
            .filter(auction_product_id__auction_end_date_time__lt=today)
            .aggregate(Sum('max_bid'))['max_bid__sum']
    ) or '---'

    counts = [products.count(), number_of_live_auctions, number_of_auctions_completed]
    sums = [sum_of_all_products_worth, sum_of_live_products_worth, sum_of_completed_products_worth]
    numerical_stat_labels = ['Total Bids', 'Live Bids', 'Completed Bids']
    auction_add_counts = (
        products
            .values('date_created')
            .annotate(count=Count('user_id'))
            .order_by()
    )
    auction_add_counts = [c['count'] for c in auction_add_counts]
    print(auction_add_counts)
    context = {
        'products': products,
        'bidders': bidders,
        'today': today,
        'numerical_stats': zip(counts, sums, numerical_stat_labels),
        'creations': creation_dates,
        'auction_add_counts': auction_add_counts
    }

    return render(request, 'accounts/dashboard.html', context)

#############################################################################
