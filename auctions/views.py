from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, listing, watchlist, bid, comments
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def index(request):
    listings = listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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

@login_required(redirect_field_name='/login')
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        cprice = request.POST["cprice"]
        imageURL = request.POST["imageURL"]
        category = request.POST["category"]
        user = request.user.username
        owner = User.objects.get(username=user)
        createlisting = listing(owner= owner, title=title,description=description,cprice=cprice,imageURL=imageURL, sprice=cprice, category=category)
        createlisting.save()
        return render(request, "auctions/create.html")
    else:
        return render(request, "auctions/create.html")

def detail(request,id):
    try:
        item = listing.objects.get(id=id)  
        username = request.user.username
        user = User.objects.get(username=username)
        added_in_watchlist = watchlist.objects.filter(user=user, list_id = id).count()

        #Retrieve the comments
        commentobj = comments.objects.filter(item = item)

        #Enable or disable the user to bid
        bidobj = bid.objects.filter(item = item).first()
        try:
            bidder = getattr(bidobj, 'bidder')
        except:
            bidder = 'None'    

        if item.active == True:
            if bidder == user:
                disabled_bid = True
            else:
                disabled_bid = False
        else:
            disabled_bid = True

        #Enable the owner to close the auction
        try:
            listing.objects.get(owner=user, id=id)
            close_visible = True
        except:
            close_visible = False

        class NewBidForm(forms.Form):
            bprice = forms.IntegerField(label="Your Bid", disabled= disabled_bid)
            

            def clean_bprice(self):
                bprice = self.cleaned_data.get('bprice')
                if bprice <= item.cprice:
                    raise forms.ValidationError("Your bid must be greater than the current price.")
                elif bprice < item.cprice + item.sprice:
                    raise forms.ValidationError("Your bid must be in the multiples of the starting price")
                return bprice

        if added_in_watchlist == 0 :
            visible = True
        else:
            visible = False

        if request.method == "POST":
            if request.POST["watchlist"] == "add":
                query = watchlist(user=user, title=item.title, description = item.description, cprice = item.cprice, imageURL = item.imageURL, list_id=item.id)
                query.save()
                return HttpResponseRedirect(reverse('detail', args=(item.id,)))
            elif request.POST["watchlist"] == "remove":
                query = watchlist.objects.filter(list_id= item.id, user=user)
                query.delete()
                return HttpResponseRedirect(reverse('detail', args=(item.id,)))
            elif request.POST["watchlist"] == "close":
                #closeAuction = listing.objects.get(item = item)
                item.active = False
                item.save()
            elif request.POST["watchlist"] == "comment_post":
                comment = request.POST["comment"]
                comobj = comments(item = item, commenter = user, comment = comment )
                comobj.save()
                return HttpResponseRedirect(reverse('detail', args=(item.id,)))

            form = NewBidForm(request.POST)
            if form.is_valid():
                    bprice = form.cleaned_data["bprice"]
                    query = listing.objects.get(id=id)
                    query.cprice = bprice
                    query.save()
                    try: 
                        bidobj = bid.objects.get(item = item)
                        bidobj.bidder = user
                        bidobj.save()
                    except:    
                        bidding = bid(bidder= user, item = item, count = 1, bprice=1)
                        bidding.save()
                    return HttpResponseRedirect(reverse('detail', args=(item.id,)))
            else:
                return render(request, "auctions/detail.html", {
                'item': item,
                'visible': visible,
                'form': form,
                'disabled_bid': disabled_bid,
                'close_visible': close_visible,
                'bidder': bidder,
                'commentobj' : commentobj
                })
        else:
            return render(request, "auctions/detail.html", {
                'item': item,
                'visible': visible,
                'form': NewBidForm(),
                'disabled_bid': disabled_bid,
                'close_visible': close_visible,
                'bidder': bidder,
                'commentobj' : commentobj
                })
    except:
        return HttpResponse("Page does not exist.")

def watchlistpage(request):
    username = request.user.username
    user = User.objects.get(username=username)
    items = watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        'listings': items
    })    

def category(request):
    men = listing.objects.filter(category= "Men")
    women = listing.objects.filter(category= "Women")
    electronics = listing.objects.filter(category= "Electronics")
    kitchen = listing.objects.filter(category= "Kitchen")
    other = listing.objects.filter(category= "Other")
    
    return render(request, "auctions/category.html", {
        'men' : men,
        'women' : women,
        'electronics' : electronics,
        'kitchen' : kitchen,
        'other' : other
    }) 
    