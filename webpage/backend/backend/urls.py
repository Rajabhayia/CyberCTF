# users_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/challenges/', include('challenges.urls')),
    path('api/usersData/', include('usersContent.urls')),
]
