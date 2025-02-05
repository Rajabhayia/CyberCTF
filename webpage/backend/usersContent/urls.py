from django.urls import path
from . import views

urlpatterns = [
    path('load_users/', views.load_users, name='load_users'),
    path('load_points/', views.load_points, name='load_points'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
