from django.contrib import admin

from .models import CustomUser, UserLanguage, Experience


admin.site.register([CustomUser, UserLanguage, Experience])
