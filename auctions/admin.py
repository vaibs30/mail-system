from django.contrib import admin
from .models import User, listing, bid, watchlist, comments

# Register your models here.

admin.site.register(User)
admin.site.register(listing)
admin.site.register(bid)
admin.site.register(watchlist)
admin.site.register(comments)