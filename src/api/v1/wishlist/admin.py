from django.contrib import admin

from .models import Wishlist, Follow


admin.site.register([Wishlist, Follow])
