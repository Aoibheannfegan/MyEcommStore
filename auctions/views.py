from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listings, Bids, Comments, Watchlist

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
        labels = {
            "title": "Title",
            "description": "Description",
            "start_bid": "Starting Bid",
            "image_url": "Image URL",
            "category": "Category",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

def index(request):
    listings = Listings.objects.filter(active=True)
    category_choices = Listings.CATEGORY_CHOICES
    return render(request, "auctions/index.html", {
        "listings": listings,
        'category_choices': category_choices,
    })

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

def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            listing = Listings(title=title, description=description, start_bid=start_bid, image_url=image_url, category=category, user=request.user)
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing
            })
        else: # if the form is not valid
            return render(request, "auctions/create.html", {
                "form": form
            })
    else: 
        return render(request, "auctions/create.html", {
            "form": NewListingForm()
        })
    

def listing_page (request, listing_id): 
    listing = Listings.objects.get(id=listing_id)
    comments = Comments.objects.filter(listing=listing).order_by('-date')
    is_authenticated = request.user.is_authenticated
    user_details = request.user
    watching = False
    if listing.current_bid is None:
        listing.current_bid = listing.start_bid
        listing.save()
    if is_authenticated:
        watching = Watchlist.objects.filter(listing=listing_id, user=request.user.id).exists()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_authenticated": is_authenticated,
        "watching": watching,
        "user_details": user_details,
        "comments": comments
    })


def remove_from_watchlist (request, listing_id):
    if request.method == "POST":
        watchlist_item = Watchlist.objects.filter(listing=listing_id, user=request.user.id).first()
        if watchlist_item:
            watchlist_item.delete()
            return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
        else:
            return render(request, "auctions/listing.html", {
                "message": "Item not on Watchlist"
            })


def add_to_watchlist (request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(id=listing_id)
        watchlist_item = Watchlist.objects.filter(listing=listing_id, user=request.user.id).first()
        if watchlist_item:
            return render(request, "auctions/listing.html", {
                "message": "Item already added Watchlist"
            })
        else:
            add = Watchlist(listing=listing, user=request.user)
            add.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))

def place_bid (request, listing_id):
    if request.method == "POST":
        bid = float(request.POST.get('bid'))
        listing = Listings.objects.get(id=listing_id)
        if bid > listing.current_bid:
            listing.current_bid = bid
            listing.save()
            update_bid = Bids(listing=listing, user=request.user, new_bid=bid)
            update_bid.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        else:
            return render(request, "auctions/listing.html", {
                "message": "Bid not high enough"
            })

def close_auction (request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(id=listing_id)
        bid_winner = Bids.objects.filter(listing=listing_id).order_by('new_bid').last()
        if bid_winner is None:
            listing.winner = listing.user
            listing.active = False
            listing.save()
        else:
            listing.winner = bid_winner.user
            listing.active = False
            listing.save()
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    
def comments (request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(id=listing_id)
        comment = request.POST.get('comment')
        add_comment=Comments(listing=listing, user=request.user, comment=comment)
        add_comment.save()
        print("Saved comment:", add_comment)
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
 
def watchlist (request):
    watching = Watchlist.objects.filter(user=request.user.id).order_by('-listing__active')
    return render(request,  "auctions/watchlist.html", {
        "watching": watching
    })

def categories(request):
    category_choices = Listings.CATEGORY_CHOICES
    return render(request,  "auctions/categories.html", {
        'category_choices': category_choices
    })

def category(request, category):
    listing_category = Listings.objects.filter(category = category, active=True)
    category_choices = Listings.CATEGORY_CHOICES
    return render(request,  "auctions/category.html", {
        'listing_category': listing_category,
        'category_choices': category_choices,
        'current_category': category,
    })