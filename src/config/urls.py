from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as yasg_url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('api.v1.accounts.urls')),
    path('products/', include('api.v1.products.urls')),
    path('complaints/', include('api.v1.complaints.urls')),

    # debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += yasg_url
