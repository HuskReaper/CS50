### IMPORTS ###
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category, User, Listing, Comment
from django.contrib.auth.decorators import login_required

### Preset views ###
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
### My views ###  
    
def index(request):
    ## Display index page if user accesses website ##
    if request.method == "GET":
        listings = Listing.objects.filter(active=True)
        categoryItems = Category.objects.all()
        return render(request, "auctions/index.html", {
            "all_listings": listings,
            "categories": categoryItems
        })
        
    ## If user has searched for category return index ONLY with that exact category ##
    else:
        category = request.POST['category']
        searched = Category.objects.get(category_title=category)
        listings = Listing.objects.filter(active=True, category=searched)
        categoryItems = Category.objects.all()
        return render(request, "auctions/index.html", {
            "all_listings": listings,
            "categories": categoryItems
        })

@login_required(login_url='/login')
def create_listing(request):
    # Return categories and render a form to the user if method is get #
    if request.method == "GET":
        categoryItems = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": categoryItems
        }) 
         
    else:
        # Create a listing item with info from the form #
        ## Get Info from form ##
        name = request.POST["name"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image_url"]
        category = request.POST["category"]
        current_user = request.user
        
        ## Create Listing. ##
        category_d = Category.objects.get(category_title=category)
        listing = Listing(
            name = name, description = description, image_url = image, price = float(starting_bid), category = category_d, owner = current_user
        )
        
        ## Save Listing to DB. ##
        listing.save()
        
        return HttpResponseRedirect(reverse(index))
    
def view_listing(request, id):
    listing = Listing.objects.get(pk=id)
    watchlisted = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    current_user = request.user

    return render(request, "auctions/view_listing.html", {
        "data": listing,
        "in_watchlist": watchlisted,
        "comments": comments,
        "user": current_user
    })

@login_required(login_url='/login')
def watchlist_add(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("view_listing",args=(id, )))

@login_required(login_url='/login')
def watchlist_remove(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("view_listing",args=(id, )))

@login_required(login_url='/login')
def watchlist(request):
    if request.method == "GET":
        user = request.user
        listings = user.watchlist.all()
        categoryItems = Category.objects.all()
        return render(request, "auctions/watchlist.html", {
            "all_listings": listings,
            "categories": categoryItems
        })

    else:
        category = request.POST['category']
        searched = Category.objects.get(category_title=category)
        listings = Listing.objects.filter(active=True, category=searched)
        categoryItems = Category.objects.all()
        return render(request, "auctions/watchlist.html", {
            "all_listings": listings,
            "categories": categoryItems
        })
        
@login_required(login_url='/login')
def your_listings(request):
    categoryItems = Category.objects.all()
    user = request.user
    listings = Listing.objects.filter(owner = user)
    return render(request, "auctions/your_listings.html", {
        "all_listings": listings,
        "categories": categoryItems
    })
    
@login_required(login_url='/login')
def won_listings(request):
    categoryItems = Category.objects.all()
    user = request.user
    listings = Listing.objects.filter(current_bidder = user, active = False)
    return render(request, "auctions/won_listings.html", {
        "all_listings": listings,
        "categories": categoryItems
    })
    
@login_required(login_url='/login')
def place_bid(request, id):
    listing = Listing.objects.get(pk=id)
    watchlisted = request.user in listing.watchlist.all()
    
    if request.method == "POST":
        post_bid = request.POST['bid']
        min_amount = listing.price
        if int(post_bid) < min_amount:
            return render(request, "auctions/view_listing.html", {
                "data": listing,
                "in_watchlist": watchlisted,
                "message": "Cannot place bid. Bid is less than current bid."
                })
            
        if request.user == listing.owner:
            return render(request, "auctions/view_listing.html", {
                "data": listing,
                "in_watchlist": watchlisted,
                "message": "Owner of auction cannot place bids."
                })
        else:
            listing.price = post_bid
            listing.current_bidder = request.user
            listing.save()
            return render(request, "auctions/view_listing.html", {
                "data": listing,
                "in_watchlist": watchlisted,
                "message": "Bid Placed!"
                })
            
@login_required(login_url='/login')
def add_comment(request, id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=id)
        message = request.POST['message']
        comment = Comment(author=user, listing=listing, text=message)
        comment.save()
        return HttpResponseRedirect(reverse("view_listing",args=(id, )))
    
@login_required(login_url='/login')
def close_auction(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        watchlisted = request.user in listing.watchlist.all()
        listing.active = False
        listing.save()
        return render(request, "auctions/view_listing.html", {
                "data": listing,
                "in_watchlist": watchlisted
                })