from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    pass

class listing(models.Model):
    category_choices = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Electronics', 'Electronics'),
        ('Kitchen', 'Kitchen'),
        ('Others', 'Others'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=20, blank=False)
    description = models.CharField(max_length=150)
    cprice = models.IntegerField(null=False)
    imageURL = models.URLField(default="https://lunawood.com/wp-content/uploads/2018/02/placeholder-image.png")
    sprice = models.IntegerField()
    category = models.CharField(
        max_length=12,
        choices=category_choices,
    )
    active = models.BooleanField(default=True)

class bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="bid_item")
    count = models.IntegerField()
    bprice = models.IntegerField()

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    cprice = models.IntegerField()
    imageURL = models.URLField()
    list_id = models.IntegerField()

class comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    item = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="comment_item")
    comment = models.CharField(max_length=150)
